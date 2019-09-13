        if rdm_prob <= probability and evil > 0:
            # throw a random between EVIL roles (TBD)
            # not implemented
            ready_players.append([player, evil_roles[0]])
            evil -= 1
        else:
            if good > 0:
                # throw a random between EVIL roles (TBD)
                # not implemented
                ready_players.append([player, good_roles[0]])
                good -= 1