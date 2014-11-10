example-poll-backend
====================
This repo stores a minimal backend that works with videogular-questions to store and return poll information.

It is to be used as a guide to the polls API. The backend database and any processing that occurs after receipt, or prior to sending, is an example and can be switched out for whatever other system is required.

API
====================

The server exposes two endpoints, a POST /vote and a GET /results/annotationId/questionId. Additonally some work is done to fix CORS problems that could occur.

The POST endpoint expects a schema similar to the vg-questions webworker:
```
{
  questionResult: questionId,
  annotation: annotationid
  result: ...
}
```

The GET endpoint returns an object of result<->vote-count pairs:
```
{
  optionOne: 5,
  cheese: 2
  last: 3
}
```

Example Setup
====================

Before use you should browse to /setup to allow the server to setup the database
