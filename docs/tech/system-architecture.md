# System Architecture

## Overview
This document outlines the high-level architecture of our delivery aggregator platform.

## Components

### Intelligence Core
The central decision-making system that optimizes delivery provider selection.

### Order Core
Manages order lifecycle and state transitions.

### Information Gateway
Handles communication with external delivery service providers.

## Architecture Diagram

```mermaid
graph TB
    subgraph Core Services
        IC[Intelligence Core]
        OC[Order Core]
        IG[Information Gateway]
    end
    
    subgraph Provider Shims
        GS[Grab Shim]
        LS[Lalamove Shim]
        JS[J&T Shim]
        DS[Delyva Shim]
    end
    
    subgraph User Interface
        MI[Merchant Interface]
        PP[Preference Panel]
    end
    
    MI --> OC
    PP --> IC
    OC --> IC
    IC --> IG
    IG --> GS & LS & JS & DS
```

## Component Details
Each component is designed to be independently scalable and maintainable.
