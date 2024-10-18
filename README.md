


# The graph ql query to get information for the tracker

query Devices {
  user {
    devices {
      id
      activated
      latitude
      longitude
      lockEnabled
      deviceType
      orientation
      serialNumber
      vehicleType
      batteryPercentage
      status {
        isConnectedToGSM
        lastPollingTimestamp
      }
      statistics {
        totalDistance
      }
      motorcycle {
        id
        brand {
          label
        }
        model {
          label
        }
      }
      statistics {
        totalDistance
        totalTime
      }
    }
  }
}


# To get the token

mutation CreateUserOrSignInWithEmailAndPassword($email: String!, $password: String!) {
  createUserOrSignInWithEmailAndPassword(email: $email, password: $password) {
    token
  }
}



# To add in config

logger:
    default: info
    logs:
        custom_components.flashbird: debug

debugpy:
  start: true
  wait: false
  port: 5678
