import json
import sys

import numpy as np
from jira import JIRA

from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

from ReadConfig import readconfig

jira_url = readconfig("JIRA", option="JURL")
jira_user = readconfig("JIRA", option="JUSER")
jira_passwd = readconfig("JIRA", option="JPASSWD")
jira_searching = readconfig("JIRA", option="SEARCH")

story_key = []
story_summary = []
story_point = []
story_sprint = []
story_subtasks = []
subtasks_key = []
subtasks_summary = []

# custom define
bug_number = []
second_test = []
custom_col = jira_searching.split(",")


def connect_jira():
    jira = JIRA(jira_url, basic_auth=(jira_user, jira_passwd))
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
        story_key.append(story_num["key"])  # story_number
        story_summary.append(story_num["fields"]["summary"])  # story_title
        story_point.append(story_num["fields"]["customfield_10028"])  # story_point
        cache_story_sprint = []
        for i in story_num["fields"]["customfield_10020"]:
            cache_story_sprint.append(i["name"])  # sprint_number
        story_sprint.append(cache_story_sprint)
        for i in story_num["fields"]["subtasks"]:
            story_subtasks.append(i)
        cache_subtasks_key = []
        cache_subtasks_summary = []
        for i in story_num["fields"]["subtasks"]:
            cache_subtasks_key.append(i["key"])  # subtask_number
            cache_subtasks_summary.append(i["fields"]["summary"])  # subtask_title
        subtasks_key.append(cache_subtasks_key)
        subtasks_summary.append(cache_subtasks_summary)

    """=====================[bug]==================================="""

    for i in np.arange(0, len(data)):
        num = 0
        for p in np.arange(0, len(subtasks_summary[i])):
            if "BUG" in subtasks_summary[i][p]:
                num = num + 1
        bug_number.append(num)

    """=====================[CUSTOMFIELD]==================================="""
    if not custom_col[0] == '':
        for i in np.arange(0, len(custom_col)):
            globals()[str(custom_col[i])] = []
            for j in np.arange(0, len(data)):
                num = 0
                for p in np.arange(0, len(subtasks_summary[j])):
                    if custom_col[i] in subtasks_summary[j][p]:
                        num = num + 1

                globals()[str(custom_col[i])].append(num)
    """=====================[CUSTOMFIELD]==================================="""


def detail_file(args):
    """
    detail存成txt file
    """

    path = 'result/sprint' + args[0] + '.txt'
    f = open(path, 'w')

    for i in np.arange(0, len(story_key)):
        f.writelines('story_sprint : ' + str(story_sprint[i]) + '\n')
        f.writelines('story_number : ' + str(story_key[i]) + '\n')
        f.writelines('story_title : ' + str(story_summary[i]) + '\n')
        f.writelines('story_point : ' + str(story_point[i]) + '\n')
        f.writelines('subtask_number : ' + str(subtasks_key[i]) + '\n')
        f.writelines('subtask_title : ' + str(subtasks_summary[i]) + '\n')

        f.write('-----------------------------------------------------\n')

    f.close()

    """=====================[visualization]==================================="""


def get_chart(args):
    """
    draw a bar chart and line chart

    x-axis : story_key
    y-axis (L) : bug_number
    y-axis (R) : story_point

    """

    # bar chart
    bar = (
        Bar(init_opts=opts.InitOpts(page_title="BUG TRACKING", theme=ThemeType.DARK, width='1500', height='400px'))
        .add_xaxis(story_key)
        .add_yaxis("bug_number", bug_number, yaxis_index=0)
        .set_series_opts(
            itemstyle_opts=opts.ItemStyleOpts(opacity=0.6),
        )
        #
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Sprint " + args[0], subtitle=''),
            legend_opts=opts.LegendOpts(is_show=True, type_='scroll'),  # 圖例
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={'interval': '0'}),
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

    if not custom_col[0] == '':
        for i in np.arange(0, len(custom_col)):
            bar.add_yaxis(custom_col[i], globals()[custom_col[i]]).set_series_opts(
                itemstyle_opts=opts.ItemStyleOpts(opacity=0.6)
            )

    # line chart
    line = (
        Line()
        .add_xaxis(story_key)
        # .add_yaxis('bug_number', bug_number, yaxis_index=1)
        .add_yaxis('story_point', story_point, yaxis_index=1)
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ]
            ),
        )
    )

    bar.overlap(line)
    bar.render(path="result/sprint" + args[0] + ".html")


def main(args):
    print("-----------------------------------Step 1 connect to JIRA ----------------------------------------")
    jql = 'type = "Story" AND summary !~ "Maintenance*" AND summary !~ "OPS*" AND Sprint = ' + \
          args[
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
    print("-----------------------------------Step 5 send a email ----------------------------------------")
    # send_email.main(args)


if __name__ == '__main__':
    """
    args = sprint_id
    """
    main(sys.argv[1:])
