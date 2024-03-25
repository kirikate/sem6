namespace Tcp;


public record struct TcpPacket(
    ushort SourcePort, 
    ushort DestinationPort, 
    uint SequenceNumber, 
    uint AcknowledgmentNumber, 
    bool Ack, 
    bool Fin, 
    bool Rst, 
    bool Syn, 
    ushort WindowSize, 
    byte[] Data)
{
    public readonly override string ToString()
    {
        return $"""
            Source port:          {SourcePort}
            Destination port:     {DestinationPort}
            SequenceNumber:       {SequenceNumber}
            AcknowledgmentNumber: {AcknowledgmentNumber}
            Ack:                  {Ack}
            Fin:                  {Fin}
            Rst:                  {Rst}
            Syn:                  {Syn}
            WindowSize:           {WindowSize}  
            Data:                 {Data}
            """;
    }
}
