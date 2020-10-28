[![Issues][issues]][issues-url]
[![License][license-shield]][license-url]

<br />
<p align="center">
  <a href="https://github.com/shridpant/mindhunters">
    <img src="static/computer.svg" alt="Logo" width="30">
  </a>
  
  <h3 align="center">Mindhunters</h3>

  <p align="center">
    A social media platform that you can trust.
    <br />
    <a href="https://github.com/shridpant/mindhunters/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/shridpant/mindhunters/issues">Report Bug</a>
    ·
    <a href="https://github.com/shridpant/mindhunters/issues">Request Feature</a>
  </p>
  <p align="center">
  Key Contributors: <a href="https://github.com/gaurav-2626">Gaurav Agrawal</a>, <a href="https://github.com/shridpant">Shrid Pant</a> and <a href="https://github.com/tdhankhar">Tarun Dhankhar</a>.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Premise](#premise)
* [About the Project](#about-the-project)
    * [Built With](#built-with)
    * [Working](#working)
    * [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Future Works](#future-works)
* [Acknowledgements](#acknowledgements)

## Premise

**Cyber bullying** has risen exponentially over the years, especially among teens. And while the traumatic experiences of the victims are well-known, little has been done by social media giants to preemptively take action. On a large scale application, merely acting on the _reported posts_ is not nearly sufficient. It is absolutely necessary to proactively participate in the prevention of cyber bullying.

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screenshot][product-screenshot]](https://github.com/shridpant/mindhunters)

`Mindhunters` is a state-of-the-art LSTM-based NLP-algorithm on which this social media platform is wrapped. It provides sophisticated detection of texts that are violent, offensive, sexist, racist, discriminant or derogatory in nature. Scores are generated using `Mindhunters`, which affect the _reputation_ of each user. The generated scores are used to provide alerts to the social media platform, which may take appropriate action against the post and/or user. 

This project was, originally, made in our participation of <a href="https://devpost.com/software/mindhunters" target="_blank">`UB Hacking 2020`</a>.

### Built With

The server-side application was built with Flask, Keras and NLTK. SQLite3 was employed for database management, and HTML, CSS and JavaScript for the client-side application. `Mindhunters` was made possible by many open-sourced libraries and frameworks.

### Working 

A _score_ is associated with each post that the users make. The _score_ is assigned by the sigmoid function in the output layer of `Mindhunters`. If the value of the _score_ is greater than the threshold (θ), then the post is considered to be inappropriate. _θ_ may be tuned between a value of 0 and 1, according to the required sensitivity. The _reputation_ of the users are determined by the _f(x)_, where _f_ is a function incorporating all the individual _scores_ of the posts for each user. Posts that are marked inappropriate decrease the _reputation_ of the users, while the other posts increase it.
While the _reputation_ system was created to work on the backend of the application, the current version of the Social Media publicly displays the _score_ assigned to each post and the _reputation_ associated with each user. In practise, however, these parameters may be used in he backend to evaluate reasonable actions, including reporting the users to law enforcement.

### Usage

The social media platform is a web application monitored by `Mindhunters` to provide safety from cyber bullying. To execute, simply:

1. Clone this repository with `git clone https://github.com/shridpant/mindhunters`. 
2. Navigate to the root folder of the project and execute `pip install -r requirements.txt` to install all dependencies.
3. Start your server with `python app.py`.
4. Open the address from your terminal on your browser. And you're all set!

The web application contains a number of desirable features. Examples:

1. Looking up other users

![Search Screenshot][search-screenshot]

2. Public profile

![Profile Screenshot][other-screenshot]

## Contributing

This project welcomes contributions and suggestions. Feel free to fork this repository or submit your ideas through `issues`.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

The entire `Mindhunters` application was built by [Gaurav Agrawal](https://www.linkedin.com/in/gaurav-agrawal-070599192/), [Shrid Pant](https://www.linkedin.com/in/shridpant/) and [Tarun Dhankhar](https://www.linkedin.com/in/tarundhankhar/). Please feel free to contact us with regards to the project!

## Future Works

We plan to extend the `Mindhunters` algorithm to identify misinformation (_fake news_). Further, we plan to include support for images, audios and videos. 

<!-- ACKNOWLEDGEMENTS -->
## Acknowledements

`Mindhunters` wouldn't be possible without the following resources:

* [Tensorflow](https://www.tensorflow.org/)
* [NLTK](https://www.nltk.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Jupyter Notebook](https://jupyter.org/)
* [Keras](https://keras.io/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Google Fonts](https://fonts.google.com/)
* [Img Shields](https://shields.io)

<!-- MARKDOWN LINKS & IMAGES -->
[issues]: https://img.shields.io/github/issues-raw/mindhunters/stockie
[issues-url]: https://github.com/shridpant/mindhunters/issues
[license-shield]: https://img.shields.io/apm/l/vim-mode
[license-url]: https://github.com/shridpant/mindhunters/blob/master/LICENSE
[product-screenshot]: static/screenshot.PNG
[search-screenshot]: static/search-screenshot.PNG
[other-screenshot]: static/other-screenshot.PNG

