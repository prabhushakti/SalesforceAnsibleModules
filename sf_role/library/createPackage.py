import subprocess

def create_unlocked_package(package_name, package_description):
    # Step 1: Create the package
    create_package_command = [
        'sfdx', 'force:package:create',
        '-n', package_name,
        '-d', package_description,
        '-t', 'Unlocked',
        '-r', 'force-app',  # Path to your source directory
        '-v', 'MyOrg'  # Alias of your authenticated org
    ]

    try:
        print("Creating unlocked package...")
        subprocess.run(create_package_command, check=True)
        print("Unlocked package created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating package: {e}")

def main():
    package_name = "MyUnlockedPackage"
    package_description = "This is a sample unlocked package created using Python."
    
    create_unlocked_package(package_name, package_description)

if __name__ == "__main__":
    main()
