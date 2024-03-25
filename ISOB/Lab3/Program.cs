
namespace Tcp;


public class Program
{
    private static void Main(string[] args)
    {
        CancellationTokenSource cancelTokenSource = new();

        Task.WaitAll(
        [
            Server.Instance.ConnectClient(cancelTokenSource.Token),
			new SynFlooder().ConnectToServer(Server.Instance.Ip, cancelTokenSource.Token),
            Client.Instance.ConnectToServer(Server.Instance.Ip, cancelTokenSource),      
        ]);
    }
}