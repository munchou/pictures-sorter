import os
import shutil
from flask import Flask, render_template, request

user_path = input("Enter the folder's path: ").lower()
# user_path = "D:/Images"

app = Flask(__name__, static_folder=user_path, static_url_path="/")

print("USER PATH:", user_path)

selected_directory = ""

images = [
    image
    for image in os.listdir(user_path)
    if image.endswith((".png", ".jpeg", ".jpg"))
]
images.sort()

total_images = len(images)
ignore_dirs = ["__pycache__", "_env", "__webp", "_", "templates"]
directories = [
    dir
    for dir in os.listdir(user_path)
    if os.path.isdir(f"{user_path}/{dir}") and dir not in ignore_dirs
]

directories.sort(key=str.lower, reverse=False)

# for image in images:
#     print(os.path.abspath(image))


image_num = 0

moved_to_folder = ""
moved_option = False
moved_index = 0


@app.route("/")
def index():
    if images:
        current_image = f"{selected_directory}{images[image_num]}"
    else:
        current_image = None

    return render_template(
        "index.html",
        selected_directory=selected_directory,
        total_images=total_images,
        image_num=image_num,
        user_path=user_path,
        current_image=current_image,
        directories=directories,
        moved_to_folder=moved_to_folder,
        moved_option=moved_option,
    )


@app.route("/move_up", methods=["POST"])
def move_up():
    if request.method == "POST":
        global moved_to_folder
        global moved_option
        global moved_index
        global image_num

        try:
            upper_dir = "/".join(f"{user_path}/{selected_directory}".split("/")[:-2])

            print("path:", f"{user_path}/{selected_directory}".split("/"))
            print("selected_directory:", selected_directory)
            print("upper_dir:", upper_dir)

            shutil.move(
                f"{user_path}/{selected_directory}{images[image_num]}",
                f"{upper_dir}",
            )
            moved_to_folder = f"{upper_dir}/{images[image_num]}"
            moved_option = True
            print("moved_to_folder:", moved_to_folder)
            moved_index = image_num
            images.pop(image_num)
            global total_images
            total_images -= 1
            if image_num == total_images:
                image_num -= 1

            if images:
                current_image = f"{selected_directory}{images[image_num]}"
            else:
                current_image = None

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )
        except Exception as e:
            return f"An error occured: {e}"


@app.route("/move_file", methods=["POST"])
def move_file():
    if request.method == "POST":
        global moved_to_folder
        global moved_option
        global moved_index
        global image_num
        move_to_directory = request.form["directory_button"]

        try:
            shutil.move(
                f"{user_path}/{selected_directory}{images[image_num]}",
                f"{user_path}/{selected_directory}{move_to_directory}",
            )
            moved_to_folder = f"{user_path}/{selected_directory}{move_to_directory}/{images[image_num]}"
            moved_option = True
            moved_index = image_num
            images.pop(image_num)
            global total_images
            total_images -= 1
            if image_num == total_images:
                image_num -= 1

            if images:
                current_image = f"{selected_directory}{images[image_num]}"
            else:
                current_image = None

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )
        except Exception as e:
            return f"An error occured: {e}"


@app.route("/undo_move", methods=["POST"])
def undo_move():
    if request.method == "POST":
        global total_images
        global moved_to_folder
        global moved_option
        global moved_index

        try:
            shutil.move(
                f"{moved_to_folder}",
                f"{user_path}/{selected_directory}",
            )
            print(f"Moved {moved_to_folder} to {user_path}")
            # images.pop(image_num)

            total_images += 1
            retrieved_img = moved_to_folder.split("/")[-1]
            images.insert(moved_index, retrieved_img)
            # if image_num == total_images:
            #     image_num -= 1
            moved_to_folder = ""
            moved_option = False

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=f"{selected_directory}{images[image_num]}",
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )
        except Exception as e:
            return f"An error occured: {e}"


@app.route("/remove_file", methods=["POST"])
def remove_file():
    if request.method == "POST":
        global image_num
        # print("Current picture:", images[image_num])

        try:
            os.remove(f"{user_path}/{selected_directory}{images[image_num]}")
            images.pop(image_num)
            global total_images
            total_images -= 1
            if image_num == total_images:
                image_num -= 1

            if images:
                current_image = f"{selected_directory}{images[image_num]}"
            else:
                current_image = None

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )
        except Exception as e:
            return f"An error occured: {e}"


@app.route("/create_folder", methods=["POST"])
def create_folder():
    if request.method == "POST":
        new_directory = request.form["folder_name"]
        # print("New directory:", new_directory)

        try:
            os.mkdir(f"{user_path}/{selected_directory}{new_directory}")

            directories = [
                dir
                for dir in os.listdir(f"{user_path}/{selected_directory}")
                if os.path.isdir(f"{user_path}/{selected_directory}{dir}")
                and dir not in ignore_dirs
            ]

            directories.sort(key=str.lower, reverse=False)

            if images:
                current_image = f"{selected_directory}{images[image_num]}"
            else:
                current_image = None

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )
        except Exception as e:
            return f"An error occured: {e}"


@app.route("/go_to_image", methods=["POST"])
def go_to_image():
    if request.method == "POST":
        input_image_number = request.form["image_number"]
        global image_num

        try:
            isinstance(int(input_image_number), int)
            if 0 < int(input_image_number) <= total_images:
                image_num = int(input_image_number) - 1
        except:
            pass

        if images:
            current_image = f"{selected_directory}{images[image_num]}"
        else:
            current_image = None

        try:
            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )
        except Exception as e:
            return f"An error occured: {e}"


@app.route("/next_image", methods=["POST"])
def next_image():
    print("Current path:", user_path)
    print("directories:", directories)
    global image_num
    image_num += 1

    return render_template(
        "index.html",
        selected_directory=selected_directory,
        total_images=total_images,
        image_num=image_num,
        current_image=f"{selected_directory}{images[image_num]}",
        directories=directories,
        moved_to_folder=moved_to_folder,
        moved_option=moved_option,
    )


@app.route("/previous_image", methods=["POST"])
def previous_image():
    print("Current path:", user_path)
    print("directories:", directories)
    global image_num
    image_num -= 1

    return render_template(
        "index.html",
        selected_directory=selected_directory,
        total_images=total_images,
        image_num=image_num,
        current_image=f"{selected_directory}{images[image_num]}",
        directories=directories,
        moved_to_folder=moved_to_folder,
        moved_option=moved_option,
    )


@app.route("/change_dir", methods=["POST"])
def change_dir():
    if request.method == "POST":

        global selected_directory
        global moved_option
        selected_directory += f'{request.form["change_directory"]}/'

        moved_option = False

        print("Current dir:", f"{user_path}/{selected_directory}")

        try:
            global directories
            global images
            global total_images
            global image_num

            images = [
                image
                for image in os.listdir(f"{user_path}/{selected_directory}")
                if image.endswith((".png", ".jpeg", ".jpg"))
            ]
            images.sort()
            total_images = len(images)

            # print(images)
            print("total_images:", total_images)

            print("directories before:", directories)

            directories = [
                dir
                for dir in os.listdir(f"{user_path}/{selected_directory}")
                if os.path.isdir(f"{user_path}/{selected_directory}{dir}")
                and dir not in ignore_dirs
            ]

            directories.sort(key=str.lower, reverse=False)

            print("NEW DIRECTORIES:", directories)

            image_num = 0

            if images:
                current_image = f"{selected_directory}{images[image_num]}"
            else:
                current_image = None

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
                moved_option=moved_option,
            )

        except Exception as e:
            return f"An error occured: {e}"


@app.route("/parent_directory", methods=["POST"])
def parent_directory():
    if request.method == "POST":
        global selected_directory

        print(
            "\tDIRECTORY before back to parent one:",
            f"{user_path}/{selected_directory}",
        )
        print(selected_directory.split("/"))

        # selected_directory = (
        #     ""
        #     if len(splitted_selected_directory) < 3
        #     else f'{selected_directory.split("/")[:-3]}/'
        # )

        selected_directory = f'{"/".join(selected_directory.split("/")[:-2])}/'

        print("selected_directory:", selected_directory)
        if selected_directory == "/":
            selected_directory = ""
            print("new selected_directory:", selected_directory)

        try:
            global directories
            global images
            global total_images
            global image_num

            images = [
                image
                for image in os.listdir(f"{user_path}/{selected_directory}")
                if image.endswith((".png", ".jpeg", ".jpg"))
            ]
            images.sort()
            total_images = len(images)

            directories = [
                dir
                for dir in os.listdir(f"{user_path}/{selected_directory}")
                if os.path.isdir(f"{user_path}/{selected_directory}{dir}")
                and dir not in ignore_dirs
            ]

            directories.sort(key=str.lower, reverse=False)

            image_num = 0

            if images:
                current_image = f"{selected_directory}{images[image_num]}"
            else:
                current_image = None

            return render_template(
                "index.html",
                selected_directory=selected_directory,
                total_images=total_images,
                image_num=image_num,
                current_image=current_image,
                directories=directories,
                moved_to_folder=moved_to_folder,
            )

        except Exception as e:
            return f"An error occured: {e}"


if __name__ == "__main__":
    app.run(debug=False)
