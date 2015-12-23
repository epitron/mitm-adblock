#!/usr/bin/env ruby
require 'epitools'

all = []

Path["list*.json"].each do |insta|
  json = insta.parse
  if bms = (json["bookmarks"] || json["articles"])
    all += bms
  end
end

unique = all.uniq{|h| h["hash"] }


puts "* Checking for differences between records with the same url..."

all.group_by{|h| h["url"]}.each do |k,vs|
  vs.each_cons(2) do |a,b|
    d = a.diff(b)
    if d.any?
      pp orig: a, diff: d
    end
  end
end

#

# puts "* Checking for duplicate urls..."
# pp unique.group_by{|h| h["url"]}.select{|k,v| v.size > 1}


puts "* Writing all unique records to merged.json"
File.write("merged.json", JSON.pretty_generate(unique))
