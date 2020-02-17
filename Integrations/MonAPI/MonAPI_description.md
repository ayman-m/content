# MonAPI Instructions

[![N|Solid](https://www.monapi.io/static/landing/assets/images/_smarty/logo_dark.b0dd7f12d774.png)](https://www.monapi.io)

You can use this integration to access MonAPI, which provides risk, check and reputation based information for digital assets like IP's, Domain's and E-Mail Addresses in their database. The integration is limited to the IP query, however the API is capable of querying the following: 

  - IP Addresses
  - Domains
  - E-Mails
  - Geolocation
  - ASN

# Authentication
The API can be accessible for not authenticated Users. You can access the API with or without API Keys within the throttling thresholds without sign up.
You can register for our public Alpha Test a new monapi.io API key at their developer portal.
monapi.io expects for the API key to be included in all API requests to the server in a header.

# IP Query
The integration Returns Threat & Geolocation Data for a given IPv4 Address
The IP API Endpoint will test an IPv4 Address against an aggregated database with more than 400 Blacklists and threat intelligence datasources. 

## API Documentation
Documentation for [Python](https://www.monapi.io/docs/?python#) and [Javascript](https://www.monapi.io/docs/?javascript#) ..

## Commands

The following commands were coded part of this integration:

| Command | Description |
| ------ | ------ |
| mon-ip-query | Get the IP address reputatio information |