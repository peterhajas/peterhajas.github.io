#!/usr/local/bin/python

import os
import sys

path_to_post = sys.argv[1]
out_dir = sys.argv[2]

# Open the post

old_post_handle = open(path_to_post, 'r')

lines = old_post_handle.readlines()

# Find the metadata area. It's from the top of the file til the second "==="

metadata_lines = [ ]
seen_equals_delims = 0

for line in lines:
    if seen_equals_delims == 2:
        break
    if line == '===\n':
        seen_equals_delims+=1
    metadata_lines.append(line)

def find_metadata_with_string(string):
    for line in metadata_lines:
        if string in line:
            return line

title_line = find_metadata_with_string("title: ")
date_line = find_metadata_with_string("created: ")

title = title_line.replace("title: ", "")
date = date_line.replace("created: ", "")

title = title.replace("\n", "")
date = date.replace("\n", "")

def find_tags_index():
    index = 0
    for line in metadata_lines:
        if line == 'tags:\n':
            return index
        index+=1

tag_lines = metadata_lines[find_tags_index():]

tags = [ ]

for tag_line in tag_lines:
    if tag_line == 'tags:\n':
        continue
    if tag_line == '===\n':
        continue
    tag = tag_line
    tag = tag.replace("\n", "")
    tag = tag.replace("- ", "")
    tags.append(tag)

# Now that we have the metadata, let's grab the rest of the post

def find_post_start_index():
    index = 0
    for line in lines:
        if '===post===' in line:
            return index+1
        index +=1

def find_post_end_index():
    index = 0
    for line in lines:
        if '===/post===' in line:
            return index
        index +=1

post_lines = lines[find_post_start_index():find_post_end_index()]

lines_to_output = []
for post_line in post_lines:
    if "{%" in post_line:
        continue
    lines_to_output.append(post_line)


# Now that we have all this data, let's find out some properties about the output post

out_file_name = date.split(' ')[0]

out_file_post_name_component = title
out_file_post_name_component = out_file_post_name_component.replace(' ', '-')
out_file_post_name_component = out_file_post_name_component.replace(',', '')
out_file_post_name_component = out_file_post_name_component.replace('.', '')
out_file_post_name_component = out_file_post_name_component.replace('?', '')
out_file_post_name_component = out_file_post_name_component.lower()

out_file_name += '-' + out_file_post_name_component
out_file_name += '.md'

# Now write the file

# Header

out_file_path = out_dir + out_file_name

out_file = open(out_file_path, 'w')

out_file.write('---\n')
out_file.write('layout: post\n')

out_file_title_line = 'title: \"{}\"'.format(title) + '\n'
out_file.write(out_file_title_line)

out_file_date_line = 'date: {} -0700'.format(date) + '\n'
out_file.write(out_file_date_line)

out_file_tags_line = 'tags: '

for tag in tags:
    out_file_tags_line += tag
    out_file_tags_line += ' '

out_file_tags_line += '\n'
out_file.write(out_file_tags_line)

out_file.write('---\n')

# Contents

for line in lines_to_output:
    out_file.write(line)
