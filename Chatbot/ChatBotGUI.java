import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ChatBotGUI extends JFrame {

    private JTextArea chatArea;
    private JTextField inputField;
    private ChatBot bot;

    public ChatBotGUI() {
        bot = new ChatBot();

        setTitle("Java AI Chatbot");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(500, 600);
        setLocationRelativeTo(null);   // Center window
        setLayout(new BorderLayout());

        // CHAT AREA
        chatArea = new JTextArea();
        chatArea.setEditable(false);
        chatArea.setFont(new Font("Arial", Font.PLAIN, 16));
        chatArea.setLineWrap(true);
        chatArea.setWrapStyleWord(true);

        JScrollPane scrollPane = new JScrollPane(chatArea);
        scrollPane.setPreferredSize(new Dimension(500, 500));
        add(scrollPane, BorderLayout.CENTER);

        // INPUT FIELD
        inputField = new JTextField();
        inputField.setFont(new Font("Arial", Font.PLAIN, 16));
        inputField.setPreferredSize(new Dimension(500, 40));
        add(inputField, BorderLayout.SOUTH);

        // Handle user input
        inputField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String userText = inputField.getText().trim();
                if (userText.isEmpty()) return;

                chatArea.append("You: " + userText + "\n");
                String botResponse = bot.getResponse(userText);
                chatArea.append("Bot: " + botResponse + "\n\n");

                inputField.setText("");
            }
        });

        // Force Swing to render properly
        SwingUtilities.invokeLater(() -> {
            revalidate();
            repaint();
            setVisible(true);
        });
    }

    public static void main(String[] args) {
        new ChatBotGUI();
    }
}
