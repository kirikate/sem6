
using System.Net;
using System.Net.Http.Headers;
using System.Net.Sockets;
using System.Text;

namespace Tcp;

public class Server
{
    private static Lazy<Server> _lazy = new(() => new Server(new(IPAddress.Parse("127.0.0.1"), 6000)));
    public static Server Instance => _lazy.Value;


    private Server(IPEndPoint ip)
    {
        Ip = ip;
    }

    public IPEndPoint Ip { get; }

    private readonly Dictionary<int, Socket> _clients = [];
	

    public async Task ConnectClient(CancellationToken token)
    {
        Socket listenerSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp) { ReceiveTimeout = 300 };

        try
        {
            listenerSocket.Bind(Ip);

            listenerSocket.Listen(15);
            Console.WriteLine($"Server start on {Ip.Port}");

            while (true)
            {
                if (token.IsCancellationRequested)
                    break;

                Socket clientSocket = await listenerSocket.AcceptAsync(token);
                // Console.WriteLine($"Client from {clientSocket.RemoteEndPoint} try to connect");

                _clients.Add(((IPEndPoint)clientSocket.RemoteEndPoint!).Port, clientSocket);

                Thread clientThread = new Thread(ProcessClient);
                clientThread.Start(((IPEndPoint)clientSocket.RemoteEndPoint).Port);
            }
        }
        catch (OperationCanceledException)
        { }
        catch (Exception ex)
        {
            Console.WriteLine($"Ошибка: {ex.Message}");
        }
    }

    private void ProcessClient(object obj)
    {
        try
        {
            int port = (int)obj;

            TcpPacket packet = Read(port);

            // first handshake
            if (packet is not { Syn: true, Data.Length: 0 })
            {
                throw new Exception($"""
                    Invalid first handshake
                    {packet}
                    """);
            }

            uint sequenceNumber = Convert.ToUInt32(Random.Shared.Next());
            uint acknowledgmentNumber = packet.SequenceNumber + 1;
            ushort windowSize = packet.WindowSize;

			Console.WriteLine(packet);

            // second handshake
            Send(port, new TcpPacket()
            {
                SourcePort = (ushort)Ip.Port,
                DestinationPort = (ushort)port,
                SequenceNumber = sequenceNumber,
                AcknowledgmentNumber = acknowledgmentNumber,
                Syn = true,
                Ack = true,
                WindowSize = windowSize,
                Data = [],
            });

            packet = Read(port);

            // Invalid third handshake
            if (packet is not { Ack: true, Data.Length: 0 })
                throw new Exception("Invalid third handshake");

            if (packet.AcknowledgmentNumber != sequenceNumber + 1)
                throw new Exception("Invalid third handshake");

            Console.WriteLine("Client successful connected\n");


            string message = "Hello client!";


            Console.WriteLine($"Server seend message: {message}\n");

            List<TcpPacket> packets = ToPackets(message.AsBytes(), windowSize, (ushort)Ip.Port, (ushort)port, sequenceNumber, acknowledgmentNumber).ToList();


            foreach (var packetToClient in packets)
            {
                Send(port, packetToClient);

                packet = Read(port);

                if (packet is not { Ack: true, Data.Length: 0 })
                    throw new Exception("Incorrect confirmation packet");

                if (packet.Rst)
                {
                    Console.WriteLine($"Emergency connection termination{packet.SourcePort}");
                    _clients[packet.SourcePort].Close();
                    return;
                }

                if (packetToClient.SequenceNumber + windowSize != packet.AcknowledgmentNumber)
                    throw new Exception("Invalid sequence number in client packet");
            }

            Send(port, new TcpPacket() 
            { 
                SourcePort = (ushort)Ip.Port, 
                DestinationPort = (ushort)port, 
                SequenceNumber = sequenceNumber, 
                AcknowledgmentNumber = acknowledgmentNumber,
                Fin = true,
                WindowSize = windowSize,
                Data = []
            });
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
        finally
        {
            int port = (int)obj;

            if (_clients[port].Connected)
                _clients[port].Close();
        }
    }

    private void Send(int port, TcpPacket packet)
    {
        byte[] responseBuffer = packet.AsBytes();
        _clients[port].Send(responseBuffer);
    }

    public TcpPacket Read(int port)
    {
        byte[] messageBuffer = new byte[4096];
        List<byte> res = [];

        int bytesRead = _clients[port].Receive(messageBuffer);
        res.AddRange(messageBuffer[0..bytesRead]);

        return res.ToArray().AsTcpPacket();
    }

    private static IEnumerable<TcpPacket> ToPackets(
        byte[] data,
        ushort windowsSize,
        ushort sourcePort,
        ushort destinationPort,
        uint sequenceNumber,
        uint acknowledgmentNumber)
    {
        for (int id = 0; id < data.Length; id += windowsSize, sequenceNumber += windowsSize)
        {
            var dataSlice = data[id..Math.Min(id + windowsSize, data.Length)];

            yield return new TcpPacket()
            {
                SourcePort = sourcePort,
                DestinationPort = destinationPort,
                SequenceNumber = acknowledgmentNumber,
                WindowSize = windowsSize,
                Data = dataSlice
            };
        }
    }
}
