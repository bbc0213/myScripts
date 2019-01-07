#!/usr/bin/perl
open(VML, "<$ARGV[0]") or die $!;
while(<VML>){
    s/caseNo="\w+"/caseNo="$ARGV[1]"/;
    s/traceId="\w+"/traceId="$ARGV[2]"/;
    $VML[$#VML+1]=$_;
}
close(VML);
open(NEWVML, ">$ARGV[3]") or die $!;
print NEWVML foreach(@VML);
close(NEWVML);
