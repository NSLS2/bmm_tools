
# There must be a better way to do this, but Bruce is too crappy of a
# programmer to know what it is.

# This file exists as a way of feeding a profile's value of RE.md
# (facility metadata, used for lots of things, including automated
# generation of file paths for file-writing IOCs) into the library of
# BMMCommon modules.
#
# The intent here is to link this scalar with RE.md as soon as RE.md
# is defined or re-defined.  For example, in BMM.user_ns.base around
# line, around line 125:
#      BMMCommon.tools.md.common_md = RE.md

# Later on, when the user is changed by a call to sync_experiment,
# this must be reset.  This is shown in BMM.user around line 877

# Then, a module in the BMMCommon library that needs this dict should
# do something like BMMCommon.devices.usb_camera around line 18
#      md = BMMCommon.tools.md.common_md

# similarly, there is a common_re:
#      BMMCommon.tools.md.common_re = RE
# which can be used throughout BMMCommon in the same manner



# This works.  No doubt this will meet with Tom's withering disapproval
# at some point.  Wouldn't be the first time <3



common_re = None
common_md = None
