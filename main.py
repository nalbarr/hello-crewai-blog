from crew import BlogWriter
from get_image import get_image
import warnings

warnings.filterwarnings("ignore")


def write_blog_post(topic: str):
    my_writer = BlogWriter()
    result = my_writer.crew().kickoff(inputs={"topic": topic})

    return result


if __name__ == "__main__":
    write_blog_post("Price Optimization with Python")
    get_image()
