import jwtDecode from "jwt-decode";

// remain access token time in seconds
function getRemainingTokenTime(jwtToken) {
    try {
        const decodedToken = jwtDecode(jwtToken);
        if (decodedToken && decodedToken.exp) {
            const expirationTimeInSeconds = decodedToken.exp;
            const currentTimeInSeconds = Math.floor(Date.now() / 1000);
            const remainingTimeInSeconds = expirationTimeInSeconds - currentTimeInSeconds;
            return remainingTimeInSeconds >= 0 ? remainingTimeInSeconds : 0;
        }
    } catch (error) {
        console.error("Error decoding JWT token:", error);
    }
    return 0;
}

export {getRemainingTokenTime}