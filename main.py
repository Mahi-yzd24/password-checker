import random
import string

# بررسی قدرت رمز عبور
def check_password_strength(password: str) -> (bool, list, list): # type: ignore
    errors = []
    successes = []

    if len(password) < 8:
        errors.append("❌ Password must be at least 8 characters.")
    else:
        successes.append("✅ Password length is appropriate.")

    if any(c.isupper() for c in password):
        successes.append("✅ Contains uppercase letter.")
    else:
        errors.append("❌ Must contain at least one uppercase letter.")

    if any(c.islower() for c in password):
        successes.append("✅ Contains lowercase letter.")
    else:
        errors.append("❌ Must contain at least one lowercase letter.")

    if any(c.isdigit() for c in password):
        successes.append("✅ Contains number.")
    else:
        errors.append("❌ Must contain at least one number.")

    special_chars = "@#$%^&*!"
    if any(c in special_chars for c in password):
        successes.append("✅ Contains special character.")
    else:
        errors.append(f"❌ Must contain at least one special character. ({special_chars})")

    is_strong = len(errors) == 0
    return is_strong, successes, errors


def generate_strong_password(length=12):
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "@#$%^!"

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]

    all_chars = lowercase + uppercase + digits + special
    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

def is_password_in_file(password, filename="save_passwords.txt"):
    try:
        with open(filename, "r") as f:
            return password in f.read().splitlines()
    except FileNotFoundError:
        return False

def save_password(password):
    save = input("Do you want to save this password to a file? (y/n): ")
    if save.lower() == 'y':
        if not is_password_in_file(password):
            with open("save_passwords.txt", "a") as f:
                f.write(password + "\n")
                print("✅ Password saved to 'save_passwords.txt'")
        else:
            print("⚠️ This password is already saved.")
    else:
        print("❎ Password not saved.")

def main():
    while True:
        print("\n=== Menu ===")
        print("1. Check password (enter manually)")
        print("2. Create strong password (auto-generate)")
        print("3. Exit")
        print("4. Enter and save your own password")  # گزینه‌ی جدید

        choice = input("Your choice (1/2/3/4): ")

        if choice == "1":
            while True:
                password = input("Enter your password (or type 'exit' to return to menu): ")
                if password.lower() == 'exit':
                    break

                strong, successes, errors = check_password_strength(password)

                print("\n🔍 Password Check Results:")
                for msg in successes:
                    print(msg)
                for msg in errors:
                    print(msg)

                if strong:
                    print("\n✅ Your password is strong.")
                else:
                    print("\n❌ Your password is weak.")

                # نمی‌خوایم پیشنهاد بدیم، چون این گزینه مخصوص بررسیه فقط
                break

        elif choice == "2":
            length = input("Optional password length (minimum 8): ")
            try:
                length = int(length)
                password = generate_strong_password(length)
                print("Created password:", password)
                strong, _, _ = check_password_strength(password)
                if strong:
                    print("✅ This password is strong.")
                    save_password(password)
                else:
                    print("⚠️ Something went wrong, this password is not strong!")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            print("Exit app. Goodbye!")
            break

        elif choice == "4":
            password = input("Enter your own password: ")
            strong, successes, errors = check_password_strength(password)

            print("\n🔍 Password Check Results:")
            for msg in successes:
                print(msg)
            for msg in errors:
                print(msg)

            if strong:
                print("✅ Your password is strong.")
            else:
                print("⚠️ Your password is weak. You can still save it if you want.")
            
            save_password(password)

        else:
            print("Invalid option. Please enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()
