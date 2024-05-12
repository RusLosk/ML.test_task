import pandas as pd
import numpy as np
from scipy.stats import variation


class ColumnStats:
    def __init__(self, col_name, col_type):
        self.col_name = col_name
        self.col_type = col_type
        self.min_val = None
        self.max_val = None
        self.mean = None
        self.median = None
        self.mode = None
        self.percent_zero_rows = None
        self.variance = None
        self.std = None
        self.interquartile_range = None
        self.coefficient_of_variation = None
        self.num_distinct_values = None


class Summarizer:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.summary_stats = []

    def calculate_summary(self):
        for col_name, col_type in self.dataframe.dtypes.items():
            if pd.api.types.is_numeric_dtype(col_type):
                column_stats = ColumnStats(col_name, col_type)
                data = self.dataframe[col_name]

                column_stats.min_val = data.min()
                column_stats.max_val = data.max()
                column_stats.mean = data.mean()
                column_stats.median = data.median()
                column_stats.mode = data.mode().values[0]
                column_stats.percent_zero_rows = (data == 0).sum() / len(data) * 100
                column_stats.variance = data.var()
                column_stats.std = data.std()
                column_stats.interquartile_range = data.quantile(0.75) - data.quantile(0.25)
                column_stats.coefficient_of_variation = variation(data)
                column_stats.num_distinct_values = data.nunique()

                self.summary_stats.append(column_stats)
            elif pd.api.types.is_string_dtype(col_type):
                data = self.dataframe[col_name]
                variety_counts = data.value_counts()

                # Appending only the variety counts
                self.summary_stats.append((col_name, variety_counts))

    def generate_report(self, output_types=('xlsx', 'markdown', 'html'), output_filenames=None):
        report_contents = {}

        for output_type in output_types:
            if output_type == 'markdown':
                report_contents['markdown'] = self._generate_markdown_report()
            elif output_type == 'html':
                report_contents['html'] = self._generate_html_report()
            elif output_type == 'xlsx':
                report_contents['xlsx'] = self._generate_xlsx_report(output_filenames['xlsx'])
            else:
                raise ValueError("Unsupported output type")

        return report_contents

    def _generate_markdown_report(self):
        report_content = "# Summary Statistics\n\n"
        for stats in self.summary_stats:
            if isinstance(stats, ColumnStats):
                report_content += f"## {stats.col_name}\n"
                report_content += f"Type: {stats.col_type}\n"
                report_content += f"Min: {stats.min_val}\n"
                report_content += f"Max: {stats.max_val}\n"
                report_content += f"Mean: {stats.mean}\n"
                report_content += f"Median: {stats.median}\n"
                report_content += f"Mode: {stats.mode}\n"
                report_content += f"Percent of Zero Rows: {stats.percent_zero_rows:.2f}%\n"
                report_content += f"Variance: {stats.variance}\n"
                report_content += f"Standard Deviation: {stats.std}\n"
                report_content += f"Interquartile Range: {stats.interquartile_range}\n"
                report_content += f"Coefficient of Variation: {stats.coefficient_of_variation}\n"
                report_content += f"Number of Distinct Values: {stats.num_distinct_values}\n\n"
            elif isinstance(stats, tuple):
                col_name, data = stats
                report_content += f"## {col_name}\n"
                report_content += "Unique Values:\n"
                for value, count in data.items():
                    report_content += f"- {value}: {count}\n"
                report_content += "\n"
        return report_content

    def _generate_html_report(self):
        report_content = "<html><body>"
        report_content += "<h1>Summary Statistics</h1>"

        for stats in self.summary_stats:
            if isinstance(stats, ColumnStats):
                report_content += f"<h2>{stats.col_name}</h2>"
                report_content += "<table>"
                report_content += "<tr><th>Statistic</th><th>Value</th></tr>"
                report_content += f"<tr><td>Type</td><td>{stats.col_type}</td></tr>"
                report_content += f"<tr><td>Min</td><td>{stats.min_val}</td></tr>"
                report_content += f"<tr><td>Max</td><td>{stats.max_val}</td></tr>"
                report_content += f"<tr><td>Mean</td><td>{stats.mean}</td></tr>"
                report_content += f"<tr><td>Median</td><td>{stats.median}</td></tr>"
                report_content += f"<tr><td>Mode</td><td>{stats.mode}</td></tr>"
                report_content += f"<tr><td>Percent of Zero Rows</td><td>{stats.percent_zero_rows:.2f}%</td></tr>"
                report_content += f"<tr><td>Variance</td><td>{stats.variance}</td></tr>"
                report_content += f"<tr><td>Standard Deviation</td><td>{stats.std}</td></tr>"
                report_content += f"<tr><td>Interquartile Range</td><td>{stats.interquartile_range}</td></tr>"
                report_content += f"<tr><td>Coefficient of Variation</td><td>{stats.coefficient_of_variation}</td></tr>"
                report_content += f"<tr><td>Number of Distinct Values</td><td>{stats.num_distinct_values}</td></tr>"
                report_content += "</table><br>"
            elif isinstance(stats, tuple):
                col_name, data = stats
                report_content += f"<h2>{col_name}</h2>"
                report_content += "<table>"
                report_content += "<tr><th>Value</th><th>Count</th></tr>"
                for value, count in data.items():
                    report_content += f"<tr><td>{value}</td><td>{count}</td></tr>"
                report_content += "</table>"

        report_content += "</body></html>"
        return report_content

    def _generate_xlsx_report(self, output_filename):
        writer = pd.ExcelWriter(output_filename)
        for stats in self.summary_stats:
            if isinstance(stats, ColumnStats):
                df = pd.DataFrame({
                    'Column Name': [stats.col_name],
                    'Column Type': [stats.col_type],
                    'Min': [stats.min_val],
                    'Max': [stats.max_val],
                    'Mean': [stats.mean],
                    'Median': [stats.median],
                    'Mode': [stats.mode],
                    'Percent of Zero Rows': [stats.percent_zero_rows],
                    'Variance': [stats.variance],
                    'Standard Deviation': [stats.std],
                    'Interquartile Range': [stats.interquartile_range],
                    'Coefficient of Variation': [stats.coefficient_of_variation],
                    'Number of Distinct Values': [stats.num_distinct_values]
                })
                df.to_excel(writer, sheet_name=stats.col_name, index=False)
            elif isinstance(stats, tuple):
                col_name, data = stats
                stats_df = pd.DataFrame({'Value': data.index, 'Count': data.values})
                stats_df.to_excel(writer, sheet_name=col_name, index=False)

        writer._save()
        return output_filename
