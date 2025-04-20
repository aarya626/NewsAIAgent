from crew import crew


def main():
    user_input = input("Enter the topic for the news summary: ")

    result = crew.kickoff(inputs={"topic": user_input})

    print("Your summarised news is: ", result)


if __name__ == "__main__":
    main()
