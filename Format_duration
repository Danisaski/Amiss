def format_duration(seconds):
    if seconds == 0:
        return "now"
    else:
        
        year = int(seconds/(365*24*3600))
        day = int(seconds%(365*24*3600)/(3600*24))
        hour = int(seconds%(365*24*3600)%(3600*24)/3600)
        minute = int(seconds%(365*24*3600)%(3600*24)%3600/60)
        second = int(seconds%(365*24*3600)%(3600*24)%3600%60)

        out = [0]*5

        if year != 0:
            if year == 1:
                out[0] = "1 year"
            else:
                out[0] = "%s years" % str(year)

        if day != 0:
            if day == 1:
                out[1] = "1 day"
            else:
                out[1] = "%s days" % str(day)
                
        if hour != 0:
            if hour == 1:
                out[2] =  "1 hour"
            else:
                out[2] =  "%s hours" % str(hour)

        if minute != 0:
            if minute == 1:
                out[3] =  "1 minute"
            else:
                out[3] =  "%s minutes" % str(minute)

        if second != 0:
            if second == 1:
                out[4] = "1 second"
            else:
                out[4] = "%s seconds" % str(second)

        sout = ""
        j = 0
        for i in range(len(out)-1,-1,-1):
            if out[i] != 0:
                sout = "and " + out[i]
                j = i
                break
        for j in range(j-1,-1,-1):
            if out[j] != 0 and sout[0] != "a":
                sout =  out[j] + ", " + sout
            elif out[j] != 0:
                sout =  out[j] + " " + sout
            
        if sout[0] == "a":
            sout = sout[4:]
    
    return sout 
