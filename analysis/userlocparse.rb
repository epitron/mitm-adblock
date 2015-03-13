#!/usr/bin/env ruby
require 'epitools'

# https://www.googleapis.com/userlocation/v1/reports/

class JSONHash < Hash

  def initialize(hash)
    super()

    hash.each do |k,v|
      self[k] = v.is_a?(Hash) ? JSONHash.new(v) : v
    end

    self
  end

  def self.load(filename)
    new JSON.parse(File.read(filename))
  end

  def [](key)
    val = super(key)

    case key
    when /[tT]imestampMs/, /TimeMs$/
      Time.at(val/1000.0)
    when /E(\d{1,2})$/
      val / $1.to_f
    else
      val
    end
  end

  def method_missing(meth, *args, &block)
    if val = self[meth.to_s]
      val
    else
      super
    end
  end

  def each
    keys.each do |key|
      yield key, self[key]
    end
  end

  def info
    map { |k,v| [k, v.respond_to?(:count) ? "#{v.count} things (#{v.class})" : v ]}.to_h
  end

end


for arg in ARGV
  # p arg
  json      = JSONHash.load arg
  batch     = json["batch"]
  activity  = batch["activityReadings"] || []
  locations = batch["locationReadings"] || []


  def ts(rec)
    Time.at rec["timestampMs"]/1000.0
  end


  def show_activity(a)
    time = ts(a)
    as = a["activities"].map { |x| "#{x["type"]}(#{x["confidence"]})" }
    puts "#{time}: #{as.join("/")}"
  end

  def show_location(l)
    time = ts(l)
  end


  activity.each do |a|
    show_activity(a)
  end

  # locations.each do |l|
  #   show_location(l)
  # end
end
