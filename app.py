from build_graph import app
from build_pdf import generate_resume
import pprint
import warnings

warnings.filterwarnings("ignore")

query="I need a professional resume for **Manab Tikadar**, a **Bachelor of Technology** student in **Electronics and Communication Engineering** at **Indian Institute of Technology (Indian School of Mines), Dhanbad**, with an **expected graduation date of May 2027** and a **GPA of 8.99**. His coursework includes **Data Structures and Algorithms (C++), Probability & Statistics, Linear Algebra, Neural Networks and Deep Learning, Convolutional Neural Networks, Digital Circuit and System Design, and Signals and Network**. He has experience as a **Member of the Robotics and AI Club** since **January 2024**, where he has developed skills in **inverse kinematics, computer vision, and microcontroller programming**. Additionally, he attended a **Drone Workshop in October 2024**, where he built a drone using a kit and learned **PID control, GPS navigation, and MissionPlanner software**. His projects include **Extracting Text Data from Documents** (Python, Flask, Machine Learning, Document Analysis) - Developed a document analysis web app with machine learning integration; **Generative AI for Dialogue Summarization** (Python, LangChain, Prompt Engineering, LLMs) - Created an LLM-based AI system for efficient summarization; **Breast Cancer Diagnosis** (Python, Scikit-learn, Machine Learning, Data Analysis) - Built a machine learning model using Random Forest to diagnose breast cancer; **Brain Tumor Detection** (Python, OpenCV, TensorFlow, Deep Learning, U-Net) - Implemented a U-Net image segmentation model for precise tumor detection; and **ROS2-Based Robotics Project** (ROS2, Gazebo, MoveIt 2, Rviz, Python, C++) - Developed an autonomous robot navigation system with **dynamic path planning, obstacle avoidance, and robotic arm manipulation**. His technical skills include programming languages such as **C, C++, Python, Matlab, and VHDL**, and technologies like **ROS2, Gazebo, MoveIt 2, Rviz, Vivado, Xilinx FPGA, Scikit-learn, TensorFlow, Pandas, NumPy, OpenCV, Flask, LangChain, Linux, Git, and Arduino**. He also has expertise in **hardware components** such as **555 Timer IC, Digital Gate ICs, 7-Segment Displays, Crystal Oscillators, and Sensors**. His conceptual knowledge covers **Machine Learning, Neural Networks, Supervised and Unsupervised Learning, Data Structures and Algorithms, Digital Logic Design, Sequential and Combinational Circuits, and Signal Processing**. As for achievements, he participated in the **eYantra Robotics Competition (2024)**, working on a **logistics cobot project**. In social engagements, he is an **active Club Member of ROBOISM - Robotronics Club of IIT Dhanbad**. His contact details include **Phone: 6296404850**, **Email: manabtikadar621@gmail.com**, **LinkedIn: linkedin.com/in/manab-tikadar-904882284**, and **GitHub: github.com/manabtikadar**."
question = "Can you create a professional resume template for Data Scientist, using the above query?"

output_pdf_dir = r"C:\Users\manab\OneDrive\Desktop\Resume_Builder\store"

inputs = {
    "question": question,
    "query": query
}

json_output = None
for output in app.stream(inputs):
    for key, value in output.items():
        pprint.pprint(f"Node '{key}': {value}")
        if "json_output" in value:
            json_output = value["json_output"]


print("\n--- Final JSON Output ---\n")
pprint.pprint(json_output)


print(f"\n -- Final pdf uploaded to directory----\n {output_pdf_dir}")
generate_resume(json_output,output_filename="Manab_tikadar.pdf")
