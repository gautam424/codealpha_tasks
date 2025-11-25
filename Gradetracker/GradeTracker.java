import java.util.ArrayList;
import java.util.Scanner;
import java.io.Serializable;

// Student class (NOT PUBLIC)
class Student implements Serializable {
    private int id;
    private String name;
    private ArrayList<Integer> grades;

    public Student(int id, String name) {
        this.id = id;
        this.name = name;
        this.grades = new ArrayList<>();
    }

    public void addGrade(int grade) {
        grades.add(grade);
    }

    public double getAverage() {
        if (grades.isEmpty()) return 0;
        int sum = 0;
        for (int g : grades) sum += g;
        return (double) sum / grades.size();
    }

    public int getHighest() {
        int max = Integer.MIN_VALUE;
        for (int g : grades) max = Math.max(max, g);
        return max;
    }

    public int getLowest() {
        int min = Integer.MAX_VALUE;
        for (int g : grades) min = Math.min(min, g);
        return min;
    }

    public String summary() {
        return "ID: " + id +
               ", Name: " + name +
               ", Grades: " + grades +
               ", Avg: " + String.format("%.2f", getAverage()) +
               ", High: " + getHighest() +
               ", Low: " + getLowest();
    }
}

// Main Class
public class GradeTracker {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Student> students = new ArrayList<>();
        int idCounter = 1;

        while (true) {
            System.out.println("\n--- Student Grade Tracker ---");
            System.out.println("1. Add Student");
            System.out.println("2. Add Grades to Student");
            System.out.println("3. Show All Reports");
            System.out.println("4. Exit");
            System.out.print("Choose: ");
            int choice = sc.nextInt();

            if (choice == 1) {
                sc.nextLine(); 
                System.out.print("Enter student name: ");
                String name = sc.nextLine();
                students.add(new Student(idCounter++, name));
                System.out.println("Student added.");

            } else if (choice == 2) {
                System.out.print("Enter student ID: ");
                int id = sc.nextInt();
                Student found = null;

                for (Student s : students) {
                    if (s.summary().contains("ID: " + id)) {
                        found = s;
                        break;
                    }
                }

                if (found == null) {
                    System.out.println("Student not found!");
                } else {
                    System.out.print("Enter grade: ");
                    int grade = sc.nextInt();
                    found.addGrade(grade);
                    System.out.println("Grade added.");
                }

            } else if (choice == 3) {
                System.out.println("\n--- Summary Report ---");
                for (Student s : students) {
                    System.out.println(s.summary());
                }

            } else if (choice == 4) {
                System.out.println("Exiting...");
                break;
            }
        }

        sc.close();
    }
}
