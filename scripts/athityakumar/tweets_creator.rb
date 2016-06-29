begin
  puts "Enter directory to our rails project : (/home/user/...) "
  dir = gets.chomp
  Dir.chdir(dir)
  puts "1: Home time-line tweets \n2: Search by key-word tweets \nEnter your choice : "
  c = gets.chomp.to_i
  if c == 1
    while true
      system "rake twitter_status:fetch_tweets"
    end
  else
    puts "Enter search query : (#technology)"
    q = gets.chomp
    while true
      system "rake 'twitter_status:fetch_tweets_search[#{q}]'"
    end
  end  
rescue
  puts "Some error."
end    