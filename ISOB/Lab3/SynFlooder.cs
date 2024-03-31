using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Tcp;

public class SynFlooder
{
    private static readonly Lazy<SynFlooder> _lazy = new(() => new SynFlooder());
    public static SynFlooder Instance => _lazy.Value;


    public async Task ConnectToServer(IPEndPoint clientIP, CancellationToken token)
    {
        await Task.Delay(500);

        SynFlood();
    //    Attack(token);
    }

    private void Attack(CancellationToken token)
    {
        Socket socket = new(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            socket.Connect(Server.Instance.Ip);

            // first handshake
            Send(socket, new TcpPacket() 
            { 
                SourcePort = (ushort)Client.Instance.Ip.Port, 
                DestinationPort = (ushort)Server.Instance.Ip.Port,
                SequenceNumber = 0,
                AcknowledgmentNumber = 0, 
                Syn = true,
                WindowSize = 4,
                Data = []
            });

            TcpPacket packet = Read(socket);

            if (packet is not { Syn: true, Ack: true })
                throw new Exception("Invalid secons handshake");

            Send(socket, new TcpPacket() 
            { 
                WindowSize = 4, 
                DestinationPort = (ushort)Client.Instance.Ip.Port, 
                SourcePort = (ushort)Server.Instance.Ip.Port,
                SequenceNumber = 1,
                AcknowledgmentNumber = 1, 
                Ack = true,
                Data = [],
            });


            for (int i = 5; i < 100; i++)
            {
                if (token.IsCancellationRequested)
                    break;

                Thread.Sleep(100);
                try
                {
                    // set RST with client port
                    Send(socket, new TcpPacket()
                    {
                        SourcePort = (ushort)Client.Instance.Ip.Port,
                        DestinationPort = (ushort)Server.Instance.Ip.Port,
                        SequenceNumber = (uint)i * 4 + 1,
                        AcknowledgmentNumber = 1,
                        Rst = true,
                        Ack = true,
                        WindowSize = 4,
                        Data = [],
                    });
                }
                catch 
                { }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Hacker error: {ex.Message}");
        }
        finally
        {
            if (socket.Connected)
                socket.Close();
        }
    }

    private void SynFlood()
    {
        Parallel.For(5, 20, (int i) =>
        {
            try
            {
                Socket socket = new(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                socket.Connect(Server.Instance.Ip);

                Send(socket, new TcpPacket() 
                { 
                    WindowSize = 4, 
                    SourcePort = (ushort)Client.Instance.Ip.Port, 
                    DestinationPort = (ushort)(6000 + i), 
                    SequenceNumber = 0, 
                    AcknowledgmentNumber = 0, 
                    Syn = true,
                    Data = []
                });
            } 
            catch
            { }
        });
    }

    private void Send(Socket socket, TcpPacket packet)
    {
        byte[] responseBuffer = packet.AsBytes();
        socket.Send(responseBuffer);
    }

    public TcpPacket Read(Socket socket)
    {
        byte[] messageBuffer = new byte[4096];
        List<byte> res = new();

        int bytesRead  = socket.Receive(messageBuffer);
        res.AddRange(messageBuffer[0..bytesRead]);

        return res.ToArray().AsTcpPacket();
    }
}

