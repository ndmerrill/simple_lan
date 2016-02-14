import java.util.Scanner;
import java.util.Map;

public class chat {
    public static final int PORT = 44242;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("A simple LAN chat program.");

        Scanner reader = new Scanner(System.in);
        System.out.print("Would you like to create a server(c) or join one(j)? ");
        String server_or_client = reader.next();

        while (!server_or_client.equals("c") && !server_or_client.equals("j")) {
            System.out.print("Please enter either 'j' or 'c': ");
            server_or_client = reader.next();
        }

        if (server_or_client.equals("j")) {
            System.out.print("Enter your name: ");
            String name = reader.next().substring(0,16);

            Client cli = new Client(name, PORT);
            Map<String, String> servers = cli.getServerList();

            if (servers.keySet().size() == 0) {
                System.out.println("No servers found");
                return;
            }
            for (String server : servers.keySet()) {
                cli.joinServer(servers.get(server));
                break;
            }

            System.out.println("connected");

            while (true) {
                String message = reader.nextLine();
                cli.send_data_raw(message);
                while (true) {
                    String recieved = cli.get_data_raw();
                    if (recieved == null) {
                        break;
                    }
                    System.out.println(recieved);
                }
            }
        }
        else {
            System.out.print("Enter the name of your server: ");
            String name = reader.next().substring(0,16);
            Server serv = new Server(name, PORT);

            while (true) {
                Map<String, String> data = serv.recieveFromAllRaw();
                for (String person : data.keySet()) {
                    if (data.get(person) != null)
                        serv.sendToAllRaw(data.get(person));
                }
            }
        }
    }

}
