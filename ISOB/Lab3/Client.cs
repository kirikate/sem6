using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;


namespace Tcp;


public class Client
{
    private static readonly Lazy<Client> _lazy = new(() => new Client(new(IPAddress.Parse("127.0.0.1"), 6001)));
    public static Client Instance => _lazy.Value;

    private Client(IPEndPoint iPEndPoint)
    {
        Ip = iPEndPoint;
    }

    public IPEndPoint Ip { get; }

    public Task ConnectToServer(IPEndPoint serverIP, CancellationTokenSource cancelTokenSource)
    {
        Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        clientSocket.Bind(Ip);

        try
        {
            clientSocket.Connect(serverIP);

            uint r1 = Convert.ToUInt32(Random.Shared.Next());

            // first handshake
            Send(clientSocket, new TcpPacket()
            {
                SourcePort = (ushort)Ip.Port,
                DestinationPort = (ushort)serverIP.Port,
                SequenceNumber = r1,
                AcknowledgmentNumber = 0,
                Syn = true,                     
                WindowSize = 4,
                Data = []
            });

            // second handshake
            TcpPacket packet = Read(clientSocket); 

            if (packet is not { Syn: true, Ack: true })
                throw new Exception("Invalid second handshake: SYN or ACK is not set.");

            if (packet.AcknowledgmentNumber != r1 + 1)
                throw new Exception("Invalid second handshake: packet AcknowledgmentNumber not equal to r1 + 1.");

            uint r2 = packet.SequenceNumber;

            // third handshake
            Send(clientSocket, new TcpPacket()
            {
                SourcePort = (ushort)Ip.Port,
                DestinationPort = (ushort)serverIP.Port,
                SequenceNumber = 1,
                AcknowledgmentNumber = r2 + 1,
                Ack = true,
                WindowSize = 4,
                Data = []
            });



            StringBuilder messageFromServer = new();

            for (packet = Read(clientSocket); !packet.Fin; packet = Read(clientSocket))
            {
                var part = packet.Data.AsString();
                Console.WriteLine($"Get message part: {part}");

                messageFromServer.Append(part);

                Thread.Sleep(200);

                Send(clientSocket, new TcpPacket() 
                { 
                    SourcePort = (ushort)Ip.Port, 
                    DestinationPort = (ushort)serverIP.Port, 
                    SequenceNumber = 1, 
                    AcknowledgmentNumber = packet.SequenceNumber + (uint)packet.Data.Length, 
                    Ack = true,
                    WindowSize = 4,
                    Data = []
                });
            }

            Console.WriteLine($"\nGet message from server: {messageFromServer}\n");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
        finally
        {
            if (clientSocket.Connected)
                clientSocket.Close();
        }

        cancelTokenSource.Cancel();
        return Task.CompletedTask;
    }

    private void Send(Socket socket, TcpPacket packet)
    {
        byte[] responseBuffer = packet.AsBytes();
        socket.Send(responseBuffer);
    }

    public static TcpPacket Read(Socket socket)
    {
        byte[] messageBuffer = new byte[4096];
        List<byte> res = new();

        int bytesRead = socket.Receive(messageBuffer);
        res.AddRange(messageBuffer[0..bytesRead]);

        return AsTcpPacket([.. res]);
    }

    public static TcpPacket AsTcpPacket(byte[] data)
    {
        return JsonSerializer.Deserialize<TcpPacket>(data.AsString())!;
    }
}







public static class Extensions
{
    public static byte[] AsBytes(this TcpPacket packet)
    {
        return JsonSerializer.Serialize(packet).AsBytes();
    }

    public static byte[] AsBytes(this string str)
    {
        return Encoding.UTF32.GetBytes(str);
    }

    public static string AsString(this byte[] bytes, int offset)
    {
        return Encoding.UTF32.GetString(bytes, 0, offset);
    }

    public static string AsString(this byte[] bytes)
    {
        return Encoding.UTF32.GetString(bytes);
    }

    public static TcpPacket AsTcpPacket(this byte[] data)
    {
        return JsonSerializer.Deserialize<TcpPacket>(data.AsString())!;
    }
}