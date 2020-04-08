import onthisday
import config

def main():
    headline = onthisday.get_otd_headline()
    print(headline)
    if config.ENVIRONMENT != "DEV":
        print("tweeting the headline")
        onthisday.tweet_headline(headline)


if __name__ == "__main__":
    main()