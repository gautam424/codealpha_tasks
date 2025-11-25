import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;


public class Student implements Serializable {
private static final long serialVersionUID = 1L;
private int id;
private String name;
private List<Double> grades;


public Student(int id, String name) {
this.id = id;
this.name = name;
this.grades = new ArrayList<>();
}


public int getId() { return id; }
public String getName() { return name; }
public List<Double> getGrades() { return grades; }


public void addGrade(double g) { grades.add(g); }


public double average() {
if (grades.isEmpty()) return 0.0;
double sum = 0.0;
for (double g : grades) sum += g;
return sum / grades.size();
}


public double highest() {
if (grades.isEmpty()) return Double.NaN;
double hi = grades.get(0);
for (double g : grades) if (g > hi) hi = g;
return hi;
}


public double lowest() {
if (grades.isEmpty()) return Double.NaN;
double lo = grades.get(0);
for (double g : grades) if (g < lo) lo = g;
return lo;
}


@Override
public String toString() {
return String.format("[%d] %s - Grades: %s | Avg: %.2f", id, name, grades, average());
}
}