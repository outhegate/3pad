# 3PAD Maths quiz
# Date 1/08/2024
# Author: Alvin Shi
import tkinter as tk  # Import the tkinter library for creating the GUI
from tkinter import messagebox  # Import messagebox for displaying pop-up messages
import random  # Import the random library for generating random numbers

# Setup the main Tkinter window
root = tk.Tk()  # Create the main application window
root.title("Math Game")  # Set the title of the window

# Load and resize the image for the login screen
try:
    image = tk.PhotoImage(file="Maths.png")  # Load the image from a file
    image = image.subsample(2, 2)  # Reduce the image size by half (both width and height)
except tk.TclError:
    # Handle the case where the image file is not found or cannot be opened
    messagebox.showerror("Image Error", "Unable to load 'Maths.png'. Please ensure the file exists.")
    root.destroy()  # Close the application if the image cannot be loaded
    exit()

image_width = image.width()  # Get the width of the resized image
image_height = image.height()  # Get the height of the resized image

# Set the window size based on the image size, with extra space for UI elements
window_width = image_width + 300  # Add extra width for other components
window_height = image_height + 250  # Add extra height for other components
root.geometry(f"{window_width}x{window_height}")  # Set the window size using the calculated dimensions
root.config(bg="#f7d4e4")  # Set the background color of the window to a light pink

# Initialize a score variable to keep track of the user's points
score = 0  # Start the score at 0

def validate_login():
    """Validate the username and password entered by the user."""
    username = entry_username.get()  # Get the username from the entry field
    password = entry_password.get()  # Get the password from the entry field

    if username == "user" and password == "pass":  # Check if the username and password are correct
        login_frame.pack_forget()  # Hide the login frame if the login is successful
        game_frame.pack(pady=20)   # Show the game frame where the math problems will be displayed
    else:
        # Show an error message if the login credentials are incorrect
        messagebox.showerror("Login Error", "Invalid username or password.")

def generate_problem(difficulty):
    """Generate a math problem based on the selected difficulty level."""
    # Define operations and number ranges for each difficulty level
    operations = {
        'Easy': (
            '+',  # Operation for Easy difficulty: Addition
            lambda: (random.randint(1, 10), random.randint(1, 10))  # Operands range for Easy
        ),
        'Medium': (
            random.choice(['-', '*']),  # Operation for Medium difficulty: Subtraction or Multiplication
            lambda: (random.randint(1, 20), random.randint(1, 10))  # Operands range for Medium
        ),
        'Hard': (
            random.choice(['/', '*']),  # Operation for Hard difficulty: Division or Multiplication
            lambda: (random.randint(1, 50), random.randint(1, 20))  # Operands range for Hard
        )
    }

    # Select the operation and generate two random numbers based on the difficulty level
    op, operands = operations[difficulty]  # Get the operation and operand generator function
    num1, num2 = operands()  # Generate two random numbers using the operand generator

    # Ensure there's no division by zero in the problem
    if op == '/':  # If the operation is division
        while num2 == 0:  # Keep generating a new number for num2 until it's not zero
            num2 = random.randint(1, 20)  # Generate a new random number for num2

    # Create a math problem as a string (e.g., "3 + 4")
    problem = f"{num1} {op} {num2}"  # Format the problem as a string

    try:
        # Safely evaluate the problem to get the correct answer
        # Using eval can be dangerous; here it's controlled since inputs are generated
        answer = eval(problem)
    except ZeroDivisionError:
        # Handle any unexpected division by zero
        answer = "Undefined"

    return problem, answer  # Return the problem string and the correct answer

def start_game():
    """Start a new math game based on the selected difficulty."""
    difficulty = difficulty_var.get()  # Get the selected difficulty level from the buttons
    problem, answer = generate_problem(difficulty)  # Generate a new math problem and answer
    problem_label.config(text=problem)  # Display the math problem on the screen
    global correct_answer  # Use a global variable to store the correct answer
    correct_answer = answer  # Store the correct answer for later comparison
 
def check_answer():
    """Check if the user's answer to the math problem is correct."""
    global score  # Use the global score variable to update the score
    try:
        # Retrieve the user's answer from the input field and convert it to an integer
        user_answer = float(entry_answer.get())  # Convert the input text to a float to handle division results
        if user_answer == correct_answer:  # Check if the user's answer matches the correct answer
            score += 1  # Increase the score by 1 for a correct answer
            messagebox.showinfo("Correct!", "Well done! Your answer is correct.")  # Show a success message
        else:
            # Show an error message with the correct answer if the user's answer is wrong
            messagebox.showerror("Incorrect", f"Sorry, the correct answer was {correct_answer}.")
        
        update_score()  # Update the score displayed on the screen
        save_score()  # Save the current score to a file
        entry_answer.delete(0, tk.END)  # Clear the input field for the next problem
        
        # End the game if the user reaches a score of 10, otherwise start a new round
        if score >= 10:  # Check if the score has reached 10
            end_game()  # End the game if the score is 10 or more
        else:
            start_game()  # Start a new game round if the score is less than 10
    except ValueError:
        # Handle cases where the user's input isn't a valid number
        messagebox.showerror("Input Error", "Please enter a valid number.")  # Show an error message

def update_score():
    """Update the score label with the current score."""
    score_label.config(text=f"Score: {score}")  # Update the text of the score label with the current score

def save_score():
    """Save the current score to a text file."""
    try:
        with open("scores.txt", "a") as file:  # Open the scores.txt file in append mode
            file.write(f"Score: {score}\n")  # Write the current score to the file, followed by a newline
    except IOError:
        # Handle file I/O errors
        messagebox.showerror("File Error", "Unable to save the score to 'scores.txt'.")

def end_game():
    """End the game when the player reaches the winning score."""
    messagebox.showinfo("Game Over", "Congratulations! You've reached a score of 10!")  # Show a congratulatory message
    problem_label.config(text="Game Over")  # Display 'Game Over' on the screen
    check_button.config(state=tk.DISABLED)  # Disable the answer check button
    entry_answer.config(state=tk.DISABLED)  # Disable the answer input field

# Create the login frame (first screen of the app)
login_frame = tk.Frame(root, bg="#f7d4e4")  # Create a frame for the login screen with a pink background
login_frame.pack(pady=20, padx=20, fill='both', expand=True)  # Pack the login frame into the window

# Load and display the image on the login screen
image_label = tk.Label(login_frame, image=image, bg="#f7d4e4")  # Create a label to display the image
image_label.grid(row=0, column=0, rowspan=4, padx=(5, 20), pady=20)  # Position the image on the left side

# Create labels and entry fields for username and password
label_username = tk.Label(login_frame, text="Username:", bg="#f7d4e4", fg="#000000", font=("Broadway", 16))  # Create a username label
label_username.grid(row=0, column=1, pady=5, padx=(10, 0), sticky='e')  # Position the username label
entry_username = tk.Entry(login_frame, bg="#edf2f4", fg="#000000", font=("Broadway", 16))  # Create an entry field for the username
entry_username.grid(row=0, column=2, pady=5, padx=(0, 10), sticky='w')  # Position the username entry field

label_password = tk.Label(login_frame, text="Password:", bg="#f7d4e4", fg="#000000", font=("Broadway", 16))  # Create a password label
label_password.grid(row=1, column=1, pady=5, padx=(10, 0), sticky='e')  # Position the password label
entry_password = tk.Entry(login_frame, show='*', bg="#edf2f4", fg="#000000", font=("Broadway", 16))  # Create an entry field for the password
entry_password.grid(row=1, column=2, pady=5, padx=(0, 10), sticky='w')  # Position the password entry field

# Create a login button that calls the validate_login function when clicked
login_button = tk.Button(
    login_frame, text="Login", command=validate_login, bg="#ffffff", fg="#000000", font=("Broadway", 16)
)  # Create a login button
login_button.grid(row=2, column=1, columnspan=2, pady=20, padx=(10, 0), sticky='w')  # Position the login button

# Instruction label with login hints for the user
instruction_label = tk.Label(
    login_frame, text="Having trouble logging in?\nUse Username: 'user' and Password: 'pass'",
    bg="#f7d4e4", fg="#000000", font=("Broadway", 12)
)  # Create an instruction label
instruction_label.grid(row=5, column=0, columnspan=3, pady=20, padx=20)  # Position the instruction label

# Create the game frame (second screen of the app after login)
game_frame = tk.Frame(root, bg="#f7d4e4")  # Create a frame for the game screen with a pink background

# Create difficulty selection radio buttons
difficulty_var = tk.StringVar(value="Easy")  # Initialize a StringVar to store the selected difficulty

# Label for difficulty selection
difficulty_label = tk.Label(
    game_frame, text="Choose difficulty:", bg="#f7d4e4", fg="#000000", font=("Broadway", 16)
)  # Create a label for difficulty selection
difficulty_label.pack(pady=10)  # Pack the difficulty label with padding

# Radio button for Easy difficulty
easy_radiobutton = tk.Radiobutton(
    game_frame, text="Easy", variable=difficulty_var, value="Easy",
    bg="#f7d4e4", fg="#000000", selectcolor="#ffffff", font=("Broadway", 14)
)  # Create an Easy difficulty radio button
easy_radiobutton.pack(anchor='w')  # Pack the Easy radio button aligned to the west (left)

# Radio button for Medium difficulty
medium_radiobutton = tk.Radiobutton(
    game_frame, text="Medium", variable=difficulty_var, value="Medium",
    bg="#f7d4e4", fg="#000000", selectcolor="#ffffff", font=("Broadway", 14)
)  # Create a Medium difficulty radio button
medium_radiobutton.pack(anchor='w')  # Pack the Medium radio button aligned to the west (left)

# Radio button for Hard difficulty
hard_radiobutton = tk.Radiobutton(
    game_frame, text="Hard", variable=difficulty_var, value="Hard",
    bg="#f7d4e4", fg="#000000", selectcolor="#ffffff", font=("Broadway", 14)
)  # Create a Hard difficulty radio button
hard_radiobutton.pack(anchor='w')  # Pack the Hard radio button aligned to the west (left)

# Button to start the game by generating the first problem
start_button = tk.Button(
    game_frame, text="Start Game", command=start_game, bg="#ffffff", fg="#000000", font=("Broadway", 16)
)  # Create a Start Game button
start_button.pack(pady=10)  # Pack the Start Game button with padding

# Label to display the math problem to the user
problem_label = tk.Label(
    game_frame, text="", font=('Broadway', 16), bg="#f7d4e4", fg="#000000"
)  # Create a label to display the math problem
problem_label.pack(pady=10)  # Pack the problem label with padding

# Entry field for the user to input their answer
entry_answer = tk.Entry(
    game_frame, font=('Broadway', 16), bg="#edf2f4", fg="#000000"
)  # Create an entry field for the user's answer
entry_answer.pack(pady=5)  # Pack the entry field with padding

# Button to check the user's answer against the correct answer
check_button = tk.Button(
    game_frame, text="Check Answer", command=check_answer, font=('Broadway', 14), bg="#ffffff", fg="#000000"
)  # Create a Check Answer button
check_button.pack(pady=10)  # Pack the Check Answer button with padding

# Label to display the user's current score
score_label = tk.Label(
    game_frame, text="Score: 0", font=('Broadway', 16), bg="#f7d4e4", fg="#000000"
)  # Create a score label
score_label.pack(pady=5, side="bottom")  # Pack the score label at the bottom with padding

# Start the GUI event loop
root.mainloop()  # Enter the main event loop to run the application
