require 'digest'

def dictionary_attack(hashed_password, dictionary_file)
  # Read the dictionary file line by line
  File.foreach(dictionary_file) do |word|
    word.strip! # Remove any trailing whitespace or newline characters
    # Hash the word using SHA-256
    hashed_word = Digest::SHA256.hexdigest(word)
    # Compare the generated hash with the provided hash
    if hashed_word == hashed_password
      puts "Password found: #{word}"
      return
    end
  end
  # If no match is found
  puts "Password not found in dictionary."
end

# Main script execution
if ARGV.length != 2
  puts "Usage: #{File.basename(__FILE__)} HASHED_PASSWORD DICTIONARY_FILE"
else
  hashed_password = ARGV[0]
  dictionary_file = ARGV[1]
  
  # Check if the dictionary file exists
  unless File.exist?(dictionary_file)
    puts "Error: Dictionary file '#{dictionary_file}' not found."
    exit
  end
  
  dictionary_attack(hashed_password, dictionary_file)
end
