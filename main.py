import onthisday

def main():
    headline = onthisday.get_otd_headline()
    print(headline)
    onthisday.tweet_headline(headline)

if __name__ == "__main__":
    main()