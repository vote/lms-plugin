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
