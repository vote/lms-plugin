_**This repository has been deprecated.** VoteAmerica staff, see the [internal documentation](https://docs.google.com/document/d/1rmiNR6ifgRjta_xnfAj6bpForJkR1lAUuK0KiAsHXRA/edit) that covers the new setup._

## [Architectural Decision Record](https://18f.gsa.gov/2021/07/06/architecture_decision_records_helpful_now_invaluable_later/)

Aidan Feldman, 3/10/22

### Context

VoteAmerica is looking to get more young folks registered to vote, first with [FutureVoter](https://futurevoter.com/), then integrating with schools to "meet students where they're at." We established partnerships with [Blackboard](https://www.blackboard.com/) and [Instructure](https://www.instructure.com/) (Canvas), and will start conversations with school administrators at the [NASPA 2022 conference](https://conference.naspa.org/).

The minimum viable product (MVP) was to get the [VoteAmerica registration form](https://www.voteamerica.com/voter-registration/) to show up in the Blackboard and Canvas learning management systems (LMSes). It turns out that most major LMSes implement a standard called [LTI 1.3](https://www.imsglobal.org/activity/learning-tools-interoperability), which gives a consistent(ish) way to do integrations of third-party tools. This meant that the VoteAmerica tool could be built once, then theoretically be compatible with all LMS platforms. The MVP was implemented in this repository as a Flask app, and it worked.

While looking to get it working with Canvas, I came across a [reference to LTI As A Service (LTIAAS)](https://community.canvaslms.com/t5/Partner-Listings/Partner-Listing-LTI-As-a-Service-LTIAAS/ta-p/490121). After a bit of testing, it was clear that LTIAAS could be used in place of the custom application. We made the switch and are deprecating this app.

### Decision

We switched to using [LTIAAS](https://ltiaas.com/) for our LTI tool offering.

### Consequences

- LTIAAS supports displaying of a page in an iframe with zero custom code.
  - The [pricing of LTIAAS](https://ltiaas.com/#pricing) seems very reasonable, especially compared to maintenance burden and direct cost of running a custom app.
  - LTI platforms pass the user's first name, last name, and email to the tool. [The custom server used that to pre-populate the form.](https://github.com/vote/lms-plugin/blob/68e6a2803b5358f16b64891afff46359522517be/src/app.py#L101-L110) Getting rid of the LTI-specific backend/page means that the form is no longer being pre-populated. This seemed like a worthwhile tradeoff.
    - If we feel strongly about doing the pre-populating, we can always implement that behind LTIAAS and [retrieve the user information from there](https://ltiaas.com/docs/api_documentation/#idtoken-endpoint).
- Good LTI support
  - LTIAAS specializes in LTI tools, meaning:
    - It should work well
    - The product, documentation, etc. should improve over time without us having to do anything
    - They are a great resource for troubleshooting
    - They (presumably) have relationships with the LMS vendors that could be leveraged
  - The LTIAAS team has been very responsive and helpful from the beginning, with a couple examples of making changes to their documentation and product immediately after issues were raised.
- The LTIAAS team is small (two people?). One the one hand, this means they are very invested in keeping clients. On the other, it's unclear how stable the business will be long term.
- We were able to set up a custom domain for our LTIAAS endpoint, meaning the service is effectively [white-labeled](https://en.wikipedia.org/wiki/White-label_product).
  - This should avoid vendor lock-in, in that we could move off of LTIAAS without schools needing to change their configuration of URLs. (This is hypothetical; there may stored tokens or something else behind the scenes that would require migration.)

---

# VoteAmerica LMS Plugin

This is a plugin to show the [VoteAmerica voter registration form](https://www.voteamerica.com/voter-registration/) in learning management systems (LMSes). It uses the [LTI 1.3](https://www.imsglobal.org/activity/learning-tools-interoperability) standard and is derived from this [Flask example](https://github.com/dmitry-viskov/pylti1.3-flask-example).

## Local setup

While the app isn't super useful to run locally (an LMS provider needs to be able to access it), you can do so with the following steps:

1. [Install Docker.](https://docs.docker.com/get-docker/)
1. Make a file for environment variables.

   ```sh
   cp .env.sample .env
   ```

1. [Generate a key](https://github.com/dmitry-viskov/pylti1.3/wiki/How-to-generate-JWT-RS256-key-and-JWKS).
1. In the `.env` file, put the contents of the `jwtRS256.key.pub` into `PUBLIC_KEY` and `jwtRS256.key` into `PRIVATE_KEY`.
1. Start the server.

   ```sh
   docker compose up --build
   ```

1. To get a publicly-accessible URL for hosted LMSes (not running on your machine) to interact with, try using [Localtunnel](https://localtunnel.github.io/www/).
   - You may want to pick a stable subdomain (with `--subdomain`) so that you don't have to modify your registrations each time.
   - Use this hostname instead of the Heroku ones below.

## LMS setup

### Blackboard

The Tool is [centrally registered](https://docs.blackboard.com/lti/lti-registration-and-deployment) as a [System placement](https://docs.blackboard.com/lti/getting-started-with-lti#lti-placements). To [register with a Blackboard Learn instance](https://help.blackboard.com/Learn/Administrator/SaaS/Integrations/Learning_Tools_Interoperability#addlti13), use the [`Application ID`](https://developer.blackboard.com/portal/applications) as the `Client ID`.

### Canvas

To add to [Canvas](https://www.instructure.com/canvas):

1. [Configure an LTI key](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-configure-an-LTI-key-for-an-account/ta-p/140)
   1. For `Key Name`, enter `VoteAmerica`
   1. Under `Method`, select `Enter URL`
   1. Fill `JSON URL` with `https://va-pylti.herokuapp.com/config/canvas.json`
   1. Click `Save`
   1. Turn `State` to `ON`
   1. Under `Details`, copy the Client ID
1. [Add the External App](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-configure-an-external-app-for-an-account-using-a-client/ta-p/202)

## Running tests

```sh
docker compose run -w /app app pytest
```
