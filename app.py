from flask import Flask, render_template, request

app = Flask(__name__)


# --- YOUR ALGORITHM LOGIC START ---
class BST:
    class Node:
        def __init__(self, key):
            self.right = None
            self.left = None
            self.val = key

    def __init__(self, head):
        self.root = self.Node(head)

    def insert(self, key):
        self.insert_recursive(self.root, key)

    def insert_recursive(self, current_node, key):
        if key < current_node.val:
            if current_node.left is None:
                current_node.left = self.Node(key)
            else:
                self.insert_recursive(current_node.left, key)
        elif key > current_node.val:
            if current_node.right is None:
                current_node.right = self.Node(key)
            else:
                self.insert_recursive(current_node.right, key)

    def sort_list(self, current_node):
        if current_node is None:
            return []
        return (
                self.sort_list(current_node.left) +
                [current_node.val] +
                self.sort_list(current_node.right)
        )


def cscan_logic(requests, disk_head, disk_size, direction=True):
    # Renamed slightly to avoid conflict with route names
    disk_end = disk_size - 1
    disk_start = 0
    disk_seek_time = 0

    bst = BST(disk_head)
    for req in requests:
        if req != disk_head and req < disk_size:
            bst.insert(req)

    # Because disk_head is the Root, these subtrees are already split correctly
    left = bst.sort_list(bst.root.left)
    right = bst.sort_list(bst.root.right)

    right.append(disk_end)
    left.insert(0, disk_start)

    if direction:
        sequence = right + left
    else:
        # Simple logic for reverse direction if needed
        sequence = left[::-1] + right[::-1]

    sequence.insert(0, disk_head)

    for i in range(1, len(sequence)):
        disk_seek_time += abs(sequence[i] - sequence[i - 1])

    return sequence, disk_seek_time


# --- YOUR ALGORITHM LOGIC END ---

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    # Default values for the form
    form_data = {
        'queue': '98, 183, 37, 122, 14, 124, 65, 67',
        'head': '53',
        'size': '200'
    }

    if request.method == 'POST':
        try:
            # 1. Get data from form
            raw_queue = request.form.get('queue')
            raw_head = request.form.get('head')
            raw_size = request.form.get('size')

            # Update form_data so user doesn't lose their input on reload
            form_data = {'queue': raw_queue, 'head': raw_head, 'size': raw_size}

            # 2. Parse inputs
            # Convert string "98, 183" -> list [98, 183]
            queue = [int(x.strip()) for x in raw_queue.split(',')]
            head = int(raw_head)
            size = int(raw_size)

            # 3. Run your Algorithm
            sequence, seek_time = cscan_logic(queue, head, size)

            # 4. Prepare result to send back to HTML
            result = {
                'sequence': sequence,
                'seek_time': seek_time,
                'disk_size': size
            }

        except ValueError:
            error = "Invalid Input! Please enter numbers only."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', result=result, error=error, form=form_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)