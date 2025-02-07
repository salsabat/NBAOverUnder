import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.swing.*;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;

/**
 * A graphical application to run the prediction model.
 */
public class PredictorApp implements ActionListener {

    /**
     * Our application window. Disposed when application exits.
     */
    private JFrame frame;

    /**
     * Input and output components.
     */
    private JTextField playerName;
    private JTextField stat;
    private JTextField moneyLine;
    private JButton predict;
    private JLabel predictionResult;

    /**
     * Construct a new application instance. Initializes GUI components, so must be
     * invoked on the
     * Swing Event Dispatch Thread. Does not show the application window (call
     * `start()` to do
     * that).
     */
    public PredictorApp() {
        frame = new JFrame("NBA Money Line Predictor");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setPreferredSize(new Dimension(450, 450));

        JPanel tempPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        JLabel playerNameQ = new JLabel("Enter Player Name:");
        playerName = new JTextField(15);
        tempPanel.add(playerNameQ);
        tempPanel.add(playerName);
        panel.add(tempPanel);

        tempPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        JLabel statQ = new JLabel("Enter Stat:");
        stat = new JTextField(10);
        tempPanel.add(statQ);
        tempPanel.add(stat);
        panel.add(tempPanel);

        tempPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        JLabel moneyLineQ = new JLabel("Enter Money Line:");
        moneyLine = new JTextField(5);
        tempPanel.add(moneyLineQ);
        tempPanel.add(moneyLine);
        panel.add(tempPanel);

        tempPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        predict = new JButton("Predict");
        predict.addActionListener(this);
        tempPanel.add(predict);
        panel.add(tempPanel);

        tempPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        predictionResult = new JLabel("Result: N/A");
        tempPanel.add(predictionResult);
        panel.add(tempPanel);

        panel.add(Box.createVerticalGlue());

        frame.add(panel);
    }

    /**
     * Start the application by showing its window.
     */
    public void start() {
        frame.pack();
        frame.setVisible(true);
    }

    /**
     * Invoked when the predict button is clicked. Checks if the inputs are valid
     * and runs the prediction model.
     *
     * @param e the event to be processed
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            String predictionJSON = getPrediction();
            String result = predictionJSON.substring(15, predictionJSON.length() - 2);
            switch (result) {
                case "-1" -> {
                    JOptionPane.showMessageDialog(frame, "That player is not in the NBA.",
                            "Invalid Input(s)", JOptionPane.ERROR_MESSAGE);
                    predictionResult.setText("Result: N/A");
                }
                case "-2" -> {
                    JOptionPane.showMessageDialog(frame, "That is not a valid statistic.",
                            "Invalid Input(s)", JOptionPane.ERROR_MESSAGE);
                    predictionResult.setText("Result: N/A");
                }
                case "-3" -> {
                    JOptionPane.showMessageDialog(frame, "That is not a valid money line.",
                            "Invalid Input(s)", JOptionPane.ERROR_MESSAGE);
                    predictionResult.setText("Result: N/A");
                }
                case "-4" -> {
                    predictionResult.setText(
                            "You should probably take the under. It is practically guaranteed.");
                }
                case "-5" -> {
                    predictionResult.setText(
                            "You should probably take the over. It is practically guaranteed.");
                }
                default -> predictionResult.setText(result);
            }
        } catch (Exception e1) {
            System.out.println(e1);
        }

    }

    /**
     * Gets the prediction of the model ran on the user inputs.
     * 
     * @param fname The first name of the player
     * @param lname The last name of the player
     * @param stat  The target statistic
     * @param line  The number to get the prediction for
     * @return The prediction result of the model
     * 
     */
    private String getPrediction() {
        String body = String.format("{\"name\": \"%s\", \"stat\": \"%s\", \"line\": \"%s\"}",
                playerName.getText().trim().toUpperCase(), stat.getText().trim().toUpperCase(),
                moneyLine.getText().trim());
        URI uri;
        URL url;
        String result;
        try {
            uri = new URI("http://127.0.0.1:8000/prediction");
            url = uri.toURL();

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            conn.setRequestProperty("Content-Type", "application/json");

            try (DataOutputStream dos = new DataOutputStream(conn.getOutputStream())) {
                dos.writeBytes(body);
            }

            try (BufferedReader bf = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                result = bf.readLine();
            }
        } catch (Exception e) {
            result = e.getMessage();
        }
        return result;
    }

    /**
     * Run an instance of PredictorApp. No program arguments are expected.
     */
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // Set Swing theme to look the same (and less old) on all operating systems.
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
            } catch (Exception ignored) {
                /* If the Nimbus theme isn't available, just use the platform default. */
            }

            // Create and start the app
            PredictorApp app = new PredictorApp();
            app.start();
        });
    }
}
