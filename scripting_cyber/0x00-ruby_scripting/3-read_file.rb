#!/usr/bin/env ruby

require 'json'  # Import the JSON module to work with JSON files

def count_user_ids(path)
  # Read and parse the JSON file
  file_content = File.read(path)
  data = JSON.parse(file_content)
  
  # Initialize a hash to count userIds
  user_id_counts = Hash.new(0)

  # Iterate through the array of objects and count userIds
  data.each do |entry|
    user_id_counts[entry["userId"]] += 1
  end

  # Sort the results by userId and print them
  user_id_counts.sort.each do |user_id, count|
    puts "#{user_id}: #{count}"
  end
end

count_user_ids("file.json")
