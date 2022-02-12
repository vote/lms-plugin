# VoteAmerica LMS Plugin

This is a plugin to show the [VoteAmerica voter registration form](https://www.voteamerica.com/voter-registration/) in learning management systems (LMSes). It uses the [LTI 1.3](https://www.imsglobal.org/activity/learning-tools-interoperability) standard and is derived from this [Flask example](https://github.com/dmitry-viskov/pylti1.3-flask-example).

## Local setup

While the app isn't super useful to run locally (an LMS provider needs to be able to access it), you can do so with:

```sh
docker-compose up --build
```

## Blackboard

The Tool is [centrally registered](https://docs.blackboard.com/lti/lti-registration-and-deployment) as a [System placement](https://docs.blackboard.com/lti/getting-started-with-lti#lti-placements). To [register with a Blackboard Learn instance](https://help.blackboard.com/Learn/Administrator/SaaS/Integrations/Learning_Tools_Interoperability#addlti13), use the [`Application ID`](https://developer.blackboard.com/portal/applications) as the `Client ID`.
