import java.util.HashMap;

public class ChatBot {

    private HashMap<String, String> responses;

    public ChatBot() {
        responses = new HashMap<>();

        // Training with common questions (Rule-Based NLP)
        responses.put("hi", "Hello! How can I help you today?");
        responses.put("hello", "Hi there! What can I do for you?");
        responses.put("how are you", "I'm just code, but I'm running perfectly!");
        responses.put("name", "I'm Java AI Chatbot created for your project.");
        responses.put("creator", "I was created by a Java developer!");
        responses.put("java", "Java is a powerful programming language.");
        responses.put("bye", "Goodbye! Have a nice day!");
        responses.put("time", "I can't check time, but I can chat anytime!");
        responses.put("thanks", "You're welcome!");

        // Add more popular FAQs
        responses.put("what is ai", "AI stands for Artificial Intelligence—machines mimicking human intelligence.");
        responses.put("what is nlp", "NLP means Natural Language Processing, the ability of computers to understand text.");
        responses.put("what is chatbot", "A chatbot is a software application used to conduct online chat conversation.");
    }

    // Simple keyword-based NLP
    public String getResponse(String userInput) {
        userInput = userInput.toLowerCase().trim();

        for (String key : responses.keySet()) {
            if (userInput.contains(key)) {
                return responses.get(key);
            }
        }

        return "I'm not trained for this question, but I’m learning!";
    }
}
