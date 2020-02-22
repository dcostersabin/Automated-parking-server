from user.models import Economy
import hashlib
from datetime import datetime
import uuid
from user.models import Venue, Agents


def createHash():
    now = str(datetime.now())
    salt = uuid.uuid4().hex
    hash = hashlib.sha256(salt.encode() + now.encode()).hexdigest()
    return hash


def createDatabase():
    total = Economy.objects.all().count()
    while total != 100:
        new = Economy()
        new.hash = createHash()
        new.value = 100
        new.save()
        total = Economy.objects.all().count()


def createVenue():
    venueInfo = [['Sabin Parking Space', 'Balaju', True, 5], ['Dcoster Parking Corner', 'Lalitpur', True, 7]]
    for venue in venueInfo:
        new_venue = Venue()
        new_venue.name = venue[0]
        new_venue.address = venue[1]
        new_venue.status = venue[2]
        new_venue.total_agent = venue[3]
        new_venue.save()
        total_agent_in_venue = Agents.objects.filter(venue=new_venue).count()
        counter = 1
        while total_agent_in_venue != new_venue.total_agent:
            new_agent = Agents()
            new_agent.id = str(new_venue.id) + "automatedParingAgent" + str(counter)
            new_agent.spaceStatus = True
            new_agent.venue = new_venue
            new_agent.booked_status = False
            new_agent.save()
            total_agent_in_venue = Agents.objects.filter(venue=new_venue).count()
            counter += 1
