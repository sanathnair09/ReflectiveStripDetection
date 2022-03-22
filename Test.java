import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Test {
    private int PORT = 8080;
    private String ADDRESS = "localhost";

    public Test() {

    }

    public void getUDPData() {

        try {
            DatagramSocket udpSocket = new DatagramSocket(this.PORT);
            byte[] buffer = new byte[2048];
            DatagramPacket packet = null;
            while (true) {
                packet = new DatagramPacket(buffer, buffer.length);

                // Step 3 : revieve the data in byte buffer.
                udpSocket.receive(packet);
                String msg = new String(buffer, 0, buffer.length);
                System.out.println(packet.getAddress() + " -  " + msg);

                buffer = new byte[2048];
            }
        } catch (Exception e) {
            System.out.println(e);
        }

    }

    public void sendUDPStuff() {
        try {
            DatagramSocket udpSocket = new DatagramSocket(this.PORT);
            byte[] buffer = new String("Hello Nano").getBytes();
            InetAddress address = InetAddress.getByName(this.ADDRESS);
            System.out.println("address: " + address + " length: " + buffer.length);
            DatagramPacket request = null;
            while (true) {
                request = new DatagramPacket(buffer, buffer.length, address, this.PORT);
                System.out.println("data: " + request.getData());
                udpSocket.send(request);
            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }

}
