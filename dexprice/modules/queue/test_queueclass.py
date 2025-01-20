
import modules.queue.queueclass as queueclass


if __name__ == "__main__":
    task_queue = queueclass.TaskQueue()

    # 添加任务示例
    task_queue.add_task(["Gv9BCH3cL4U4YV6SJKb5H5U4kF2XoJ8KvNfuDoEYmHUQ"])
    task_queue.add_task(["JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr"])

    # 从队列中获取任务
    task = task_queue.get_task()

    # 标记任务完成
    task_queue.task_done()

    # 检查队列状态
    print(f"Is queue empty? {task_queue.is_empty()}")
    print(f"Queue size: {task_queue.size()}")
