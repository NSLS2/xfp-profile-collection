### Bluesky upgrade acceptance test
#### XFP (17-BM) HT setup

XFP uses a few different devices that come in and out of the beamline. Most of our work is done with a device we call the HT apparatus, so acceptance tests focus on that.

**Steps:**
1. Verify that HTGui starts correctly (HTgui.show())
2. Verify that Excel import of exposure plans works.
3. Verify, ***in test mode***, that an exposure run kicks off and works correctly, including color state changes for QT widgets
4. Verify that csv metadata is correctly exported and written to disk as specified
5. Verify, in test mode, that an automated alignment scan functions fully – plots correctly, calculates peak statistics, and writes the ht_coords.csv file correctly.

Other tests can be performed if time and configuration permit.
