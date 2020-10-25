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
    * [Usage](#usage)
* [Contrubuting](#contributing)
* [License](#license)
* [Contact](#contact)
* [Future Works](#future-works)
* [Acknowledgements](#acknowledgements)

## Premise

Cyber bullying has risen exponentially over the years, especially among teens. And while the traumatic experiences of the victims are well-known, little has been done by social media giants to preemptively take action. On a large scale application, merely acting on "reported posts" is not nearly sufficient. It is absolutely necessary to proactively participate in the prevention of cyber bullying.

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screenshot][product-screenshot]](https://github.com/shridpant/mindhunters)

`Mindhunters` is a state-of-the-art LSTM-based NLP-algorithm on which this social media platform is wrapped. It provides sophisticated detection of texts that are violent, offensive, sexist, racist, discriminant or derogatory in nature. Scores are generated using `Mindhunters`, which affect the "Reputation" of each user. The generated scores are used to provide alerts to the social media platform, which may take appropriate action against the post and/or user. 

This project was made in our participation of `UB Hacking 2020`.

### Built With

The server-side application was built with Flask, Keras and NLTK. Other resources included SQLite3 for database management, and HTML, CSS and JavaScript for the client-side application. Mindhunters was made possible by many open-sourced libraries and frameworks.

### Usage

The social media platform is a web application monitored by `Mindhunters` to provide safety from cyber bullying. To execute, simply:

1. Clone this repository with `git clone https://github.com/shridpant/mindhunters`. Please ensure that you have all the dependencies from `requirements.txt` installed.
2. Start your server with `python app.py`.
3. Open the address from your terminal on your browser. And you're all set!

The web application contains a number of extra features. Examples:

1. Looking up other users

[![Search Screenshot][search-screenshot]]

2. Public profile

[![Profile Screenshot][other-screenshot]]

## Contributing

This project welcomes contributions and suggestions. Feel free to fork this repository or submit your ideas through `issues`.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

The entire `Mindhunters` application was built by [Gaurav Agrawal](https://www.linkedin.com/in/gaurav-agrawal-070599192/), [Shrid Pant](https://www.linkedin.com/in/shridpant/) and [Tarun Dhankhar](https://www.linkedin.com/in/tarundhankhar/). Please feel free to contact any of us to discuss the project!

## Future Works

We plan to extend the `Mindhunters` algorithm to include images, audios and videos. In text-based analysis, `Mindhunter` can be extended to the identification of misinformation ("fake news").

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

