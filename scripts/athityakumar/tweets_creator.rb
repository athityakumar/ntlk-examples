begin
  puts "Enter directory to our rails project : (/home/user/...) "
  dir = gets.chomp
  Dir.chdir(dir)
  while true
    system "rake twitter_status:fetch_tweets"
  end
rescue
  puts "Some error."
end    