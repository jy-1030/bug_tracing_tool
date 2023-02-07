import json
import sys

import numpy as np
from jira import JIRA

from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

story_key = []
story_summary = []
story_point = []
story_sprint = []
story_subtasks = []
subtasks_key = []
subtasks_summary = []

bug_number = []
second_test = []


def connect_jira():
    jira = JIRA(' https://zerologix.atlassian.net/',
                basic_auth=('elena.peng@zerologix.com', 'mL6DrVKAZhkdcNLwZoLx84AC'))

    return jira


def json_to_file(issue_ticket, args):
    """
    download json file from jira

    """
    # Serializing json
    json_object = json.dumps(issue_ticket)

    # Writing to sample.json
    with open("data/sample" + args[0] + ".json", "w") as outfile:
        outfile.write(json_object)


def read_json_file(args):
    """
    1. parse what we need
    2. group by bug_number, 2nd execution_number
    """
    with open('data/sample' + args[0] + '.json', 'r') as f:
        data = json.load(f)

    for story_num in data:
        story_key.append(story_num["key"])
        story_summary.append(story_num["fields"]["summary"])
        story_point.append(story_num["fields"]["customfield_10028"])
        cache_story_sprint = []
        for i in story_num["fields"]["customfield_10020"]:
            cache_story_sprint.append(i["name"])
        story_sprint.append(cache_story_sprint)
        for i in story_num["fields"]["subtasks"]:
            story_subtasks.append(i)
        cache_subtasks_key = []
        cache_subtasks_summary = []
        for i in story_num["fields"]["subtasks"]:
            cache_subtasks_key.append(i["key"])
            cache_subtasks_summary.append(i["fields"]["summary"])
        subtasks_key.append(cache_subtasks_key)
        subtasks_summary.append(cache_subtasks_summary)

    """=====================[bug]==================================="""

    # bug_number = []
    for i in np.arange(0, len(data)):
        num = 0
        for p in np.arange(0, len(subtasks_summary[i])):
            if "BUG" in subtasks_summary[i][p]:
                num = num + 1
        bug_number.append(num)

    """=====================[QA]==================================="""
    # second_test = []
    for i in np.arange(0, len(data)):
        num = 0

        for p in np.arange(0, len(subtasks_summary[i])):
            if "2nd" in subtasks_summary[i][p]:
                num = num + 1
        second_test.append(num)


def detail_file(args):
    """
    detail存成txt file
    """

    path = 'result/sprint' + args[0] + '.txt'
    f = open(path, 'w')

    for i in np.arange(0, len(story_key)):
        f.writelines('story_sprint : ' + str(story_sprint[i]) + '\n')
        f.writelines('story_number : ' + str(story_key[i]) + '\n')
        f.writelines('story_point : ' + str(story_point[i]) + '\n')
        f.writelines('subtask_number : ' + str(subtasks_key[i]) + '\n')
        f.writelines('subtask_title : ' + str(subtasks_summary[i]) + '\n')

        f.write('-----------------------------------------------------\n')

    f.close()

    """=====================[visualization]==================================="""


def get_chart(args):
    """
    draw a bar chart and line chart

    x axis : story_key
    y axis (L) : bug_number
    y axis (R) : story_point

    """

    # bar chart
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(story_key)
        .add_yaxis("bug_number", bug_number, yaxis_index=0)
        .add_yaxis("2nd_test_execution", second_test, yaxis_index=0)

        #
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Sprint " + args[0], subtitle=''),
            legend_opts=opts.LegendOpts(is_show=True, type_='scroll'),  # 圖例
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                name="bug_number",
                position="left",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )

        # 延伸軸
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="story point",
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
    )

    # line chart
    line = (
        Line()
        .add_xaxis(story_key)
        # .add_yaxis('bug_number', bug_number, yaxis_index=1)
        .add_yaxis('story_point', story_point, yaxis_index=1)
    )

    bar.overlap(line)
    bar.render(path="result/sprint" + args[0] + ".html")


def main(args):
    print("-----------------------------------Step 1 connect to JIRA ----------------------------------------")
    jql = 'project = "LP1" AND type = "Story" AND summary !~ "Maintenance*" AND summary !~ "OPS*" AND Sprint = ' + args[
        0] + ' ORDER BY created DESC'
    print(jql)
    ticket = connect_jira().search_issues(jql, maxResults=200, json_result=True)
    issue_ticket = ticket['issues']

    print("-----------------------------------Step 2 download json ----------------------------------------")
    json_to_file(issue_ticket, args)

    print("-----------------------------------Step 3 analyzing ----------------------------------------")
    read_json_file(args)
    detail_file(args)

    print("-----------------------------------Step 4 draw a chart ----------------------------------------")
    get_chart(args)


if __name__ == '__main__':
    """
    args = sprint_id
    """
    main(sys.argv[1:])
