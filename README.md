# Retro Video Store API 

## Skills Assessed

- Following directions and reading comprehension
- Demonstrating understanding of the client-server model, request-response cycle and conventional RESTful routes
- Driving development with independent research, experimentation, and collaboration
- Using Postman as part of the development workflow
- Using git as part of the development workflow

- Working with the Flask package:
    - Creating models
    - Creating conventional RESTful CRUD routes for models
    - Reading query parameters to create custom behavior
    - Create unconventional routes for custom behavior
    - Creating a many-to-many relationship between two models

## Goal

Once upon a time in ye olden days to watch a movie a person had to head down to their local video store and rent a video.  We are going to step into the shoes of this old timey retro video store owner and build for ourselves all of the tools that we need in order to run our successful corner video store.  

For Part 1 of the project (which will be built in this repository) we will need a Video Store API to handle the back end. 

In keeping with our retro vibe, for Part 2 of the project (which has [it's own repository](https://github.com/AdaGold/video-store-cli)), we will build a Command Line Interface (CLI) for the front end.

The full functionality is spelled out further in the "Project Directions" files (linked below). At a high-level, our goal is to create a video store API with the following minimum functionality:
- Customers, all CRUD actions
- Videos, all CRUD actions
- Video rental checkout, custom endpoint
- Video rental check in, custom endpoint
- Listing videos checked out to a customer, custom endpoint
- Listing customers who have checked out a video, custom endpoint

## Postman Tests instead of Pytest

This project is designed to be more open ended than anything you've written in the past.  To that end, we will not be giving you Pytest tests like we have on previous projects.  We invite you to write your own tests, using the tests from Task List as a framework, but writing tests is not a required part of the project.  We will provide a suite of Postman (Smoke) tests, which are scripts that can be run inside of Postman to test your API. 

### Smoke Tests

#### What are Smoke Tests?
APIs are made to be used in combination with other apps. Think back to other projects where we've used an API. Wouldn't it be nice if we had tests that made sure an API was working as intended?

To this end, we have provided a set of [smoke tests](http://softwaretestingfundamentals.com/smoke-testing/) written in Postman to exercise all the endpoints.

Smoke tests are a *type of automated test.* The responsibility of smoke tests is to use more language/tool-agnostic set of test cases and to verify if something works very broadly. They are written to be fast and to check the most important features of an app.

Our smoke tests are *not* written in Python. They are formatted in JSON, and we will use Postman to run them (and not `pytest`.) This layer of testing helps us test that the API works, without relying on Python's Pytest.

<details>
  <summary>Want a little bit more explanation about smoke tests, unit tests, integration tests?</summary>

  The tests we've been using before this are *unit tests.* Unit tests are focused on testing small, detailed features within the same code base as the app. Our unit tests are usually written in the same language as our implementation code.

  We can imagine that unit tests feel like a detailed checklist that helps us verify that our code is correct-- we have lab coats, we observe our app in the labratory, and we check things one-by-one off a clipboard.

  Smoke tests are intentionally written to be more vague and loose. We can also think of them as a kind of [*integration test*](https://en.wikipedia.org/wiki/Integration_testing), or tests that check to make sure one or more systems are correct, from an "outside perspective."

  Our smoke tests are integration tests because they are run in Postman, and they will not be detailed about the Flask app's implementation. (They don't even are that our app was written with Flask or Python.) They will only check that for a given request, it comes back with a specific response.
</details>

### How do we use Smoke Tests?

The smoke tests will verify that your API looks correct to the outside world, by sending actual HTTP requests to your running server and checking the results. They test things like:

- Did I get a success response for a valid request?
- Did the API return JSON?
- Does the JSON contain the expected property names?

The smoke tests live in the [test folder](postman-tests). To run them:

#### Import the Smoke Tests

1. Open Postman
1. Click `Import` in the top left
1. Drag-and-drop the file into the box
1. In the left sidebar, click on the `Collections` tab

#### Run the Smoke Tests
1. Run your server. You'll need a running server open before Postman can reach any of your endpoints.
1. Explore! There are ways to run the whole collection of tests and ways to run each individual test.
1. To run a collection of tests:
    1. Click the blue `Run` button. This will launch the collection runner.
    1. In the collection runner, scroll down in the center pane and click the blue `Start Test` button

## How to Complete and Submit

Go through the waves one-by-one and build the features of this API.

At submission time, no matter where you are, submit the project via Learn.

## Project Directions

1. [Setup](ada-project-docs/setup.md)
1. [Hints and suggestions](ada-project-docs/hints.md)
1. [Wave 1: CRUD for two models](ada-project-docs/wave_01.md)
1. [Wave 2: Custom endpoints](ada-project-docs/wave_02.md)
1. [Wave 3: Optional extensions](ada-project-docs/wave_03.md)
