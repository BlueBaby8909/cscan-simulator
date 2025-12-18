from flask import Flask, render_template, request

app = Flask(__name__)


# --- ALGORITHM LOGIC ---
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


def cscan_logic(requests, disk_head, disk_size, direction):
    disk_end = disk_size - 1
    disk_start = 0
    disk_seek_time = 0

    bst = BST(disk_head)
    for req in requests:
        if req != disk_head:
            bst.insert(req)

    # Get sorted lists
    left = bst.sort_list(bst.root.left)
    right = bst.sort_list(bst.root.right)

    # Add markers (End/Start) based on standard boundaries
    # Note: These markers are added to the list, but their use depends on direction below
    right.append(disk_end)
    left.insert(0, disk_start)

    if direction == '1':  # Positive (Right/Up)
        # Logic: Head -> Right End -> Jump to 0 -> Left Part
        sequence = right + left
    else:  # Negative (Left/Down)
        # Logic: Head -> Left Start -> Jump to End -> Right Part (Reversed)
        # left includes 0 at index 0. left[::-1] makes it [..., 0]
        # right includes End at last index. right[::-1] makes it [End, ...]
        sequence = left[::-1] + right[::-1]

    sequence.insert(0, disk_head)

    # Calculate Seek Time
    for i in range(1, len(sequence)):
        disk_seek_time += abs(sequence[i] - sequence[i - 1])

    return sequence, disk_seek_time


# --- ROUTE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    # Default State
    form_data = {
        'queue': '98, 183, 37, 122, 14, 124, 65, 67',
        'head': '53',
        'size': '200',
        'direction': '1'  # Default to Positive (1)
    }

    if request.method == 'POST':
        try:
            raw_queue = request.form.get('queue')
            raw_head = request.form.get('head')
            raw_size = request.form.get('size')
            direction = request.form.get('direction')  # '1' for Positive, '0' for Negative

            form_data = {'queue': raw_queue, 'head': raw_head, 'size': raw_size, 'direction': direction}

            queue = [int(x.strip()) for x in raw_queue.split(',')]
            head = int(raw_head)
            size = int(raw_size)

            sequence, seek_time = cscan_logic(queue, head, size, direction)

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