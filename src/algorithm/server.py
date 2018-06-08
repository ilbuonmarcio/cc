import multiprocessing
import CC

if __name__ == "__main__":
    p = multiprocessing.Process(target=CC.create_cc_instance, args=(0, 1, 1))
    p.start()
