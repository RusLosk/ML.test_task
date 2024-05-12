import pandas as pd
import os
from summarizer import Summarizer


def main():
    dataframe = pd.read_excel('C:/#Python FILES for ML/DATA/iris.xlsx')

    summarizer = Summarizer(dataframe)
    summarizer.calculate_summary()

    output_directory = 'C:/#Python FILES for ML/SUMMARY'
    markdown_output_filename = 'summary_report.md'
    html_output_filename = 'summary_report.html'
    xlsx_output_filename = 'summary_report.xlsx'

    output_filenames = {
        'xlsx': os.path.join(output_directory, xlsx_output_filename)
    }

    report_contents = summarizer.generate_report(output_filenames=output_filenames)

    with open(os.path.join(output_directory, markdown_output_filename), 'w') as markdown_file:
        markdown_file.write(report_contents['markdown'])

    with open(os.path.join(output_directory, html_output_filename), 'w') as html_file:
        html_file.write(report_contents['html'])

    print(f"Reports saved to: {output_directory}")


if __name__ == "__main__":
    main()
