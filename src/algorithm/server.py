import multiprocessing
import algorithm

if __name__ == "__main__":
    p = multiprocessing.Process(target=algorithm.create_cc_instance, args=(0, 1, 1))
    p.start()
