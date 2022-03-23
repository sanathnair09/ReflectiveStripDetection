import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Test {
    private int PORT = 8080;
    private String SEND_IP = "192.168.86.27";

    private DatagramSocket udpSocket;

    public Test() {
        try {
            udpSocket = new DatagramSocket(this.PORT);
            System.out.println("stuff made");

        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("error: " + e);
        }

    }//

    public void getUDPData() {
        try {
            byte[] buffer = new byte[2048];
            DatagramPacket packet = null;
            while (true) {
                System.out.println("stuff working");

                packet = new DatagramPacket(buffer, buffer.length);

                // Step 3 : revieve the data in byte buffer.
                udpSocket.receive(packet);
                String msg = new String(buffer, 0, buffer.length);
                System.out.println(packet.getAddress() + " -  " + msg);

            }
        } catch (Exception e) {
            System.out.println(e);
        }

    }

    public void sendUDPStuff() {
        try {
            byte[] buffer = new String("Hello Nano").getBytes();
            InetAddress address = InetAddress.getByName(this.SEND_IP);
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
