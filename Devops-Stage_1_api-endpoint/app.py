from flask import Flask, jsonify, request
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    num_str = str(n)
    num_digits = len(num_str)
    armstrong_sum = sum(int(digit) ** num_digits for digit in num_str)
    return armstrong_sum == n

# Function to check if a number is perfect
def is_perfect(n):
    if n <= 0:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

# Modify endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')  # Get number parameter from URL
    if number_str is None:
        return jsonify({"error": "Number parameter is required"}), 400

    try:
        number = int(number_str)
    except ValueError:
        return jsonify({"error": "Invalid integer, please provide a valid one"}), 400

    # Initializing properties
    properties = []
    is_prime_result = is_prime(number)
    is_armstrong_result = is_armstrong(number)
    is_perfect_result = is_perfect(number)
    digit_sum = sum(int(digit) for digit in str(number))

    # Check for properties
    if is_armstrong_result:
        properties.append("armstrong")
    properties.append("even" if number % 2 == 0 else "odd")

    fun_fact = fetch_fun_fact(number)  # Assuming you implement this

    #create response object
    response = {
        "number": number,
        "is_prime": is_prime_result,
        "is_perfect": is_perfect_result,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    return jsonify(response), 200

def fetch_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", f" No fact found for {n}")
    except:
        return "could not fetch {n}, is not a fun number!"

if __name__ == '__main__':
    app.run(debug=True)

